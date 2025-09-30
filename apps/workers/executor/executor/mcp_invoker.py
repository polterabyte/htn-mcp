import json, hashlib, subprocess, shlex, requests, time as _t
from typing import Dict, Any, Tuple
from prometheus_client import Counter, Histogram, Gauge
MCP_RETRIES = Counter("mcp_call_retries_total", "Total MCP retries", ["server","tool"])
MCP_CB_OPEN = Gauge("mcp_circuit_open", "Circuit breaker open state (1=open,0=closed)", ["server","tool"])
MCP_CB_TRIPS = Counter("mcp_circuit_trips_total", "Circuit breaker trips", ["server","tool"])
MCP_SPAWN_LATENCY = Histogram("mcp_stdio_spawn_seconds", "STDIO server spawn latency", ["server"])
class MCPInvoker:
    def __init__(self, http_map: Dict[str, str], stdio_map: Dict[str, str], call_timeout=15, max_retries=1):
        self.http_map = http_map; self.stdio_map = stdio_map; self.call_timeout = call_timeout; self.max_retries = max_retries; self.cb = {}
    def _hash_inputs(self, server_id: str, tool: str, params: Dict[str, Any]) -> str:
        h = hashlib.sha256(); h.update(server_id.encode()); h.update(tool.encode()); h.update(json.dumps(params, sort_keys=True).encode()); return h.hexdigest()
    def call(self, fqid: str, params: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        assert fqid.startswith("mcp://")
        body = fqid[len("mcp://"):]; server_and_tool, _, version = body.partition("@"); server_id, _, tool = server_and_tool.partition("/")
        key = self._hash_inputs(server_id, tool, params)
        if server_id in self.http_map:
            base = self.http_map[server_id].rstrip("/"); url = f"{base}/call/{tool}"
            st = self.cb.get((server_id, tool), {'open':False,'until':0}); now = _t.time()
            if st.get('open') and now < st.get('until',0): MCP_CB_OPEN.labels(server=server_id, tool=tool).set(1); raise RuntimeError('circuit_open')
            MCP_CB_OPEN.labels(server=server_id, tool=tool).set(0)
            last_err=None
            for attempt in range(self.max_retries+1):
                try:
                    r = requests.post(url, json={"params": params}, timeout=self.call_timeout); r.raise_for_status(); return r.json(), key
                except Exception as e:
                    last_err=e
                    if attempt < self.max_retries: MCP_RETRIES.labels(server=server_id, tool=tool).inc(); _t.sleep(min(0.2*(attempt+1),1.0))
                    else: self.cb[(server_id,tool)]={'open':True,'until': now+5}; MCP_CB_TRIPS.labels(server=server_id, tool=tool).inc(); MCP_CB_OPEN.labels(server=server_id, tool=tool).set(1); raise
        if server_id in self.stdio_map:
            t0=_t.time(); proc = subprocess.Popen(shlex.split(self.stdio_map[server_id]), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True); MCP_SPAWN_LATENCY.labels(server=server_id).observe(_t.time()-t0)
            req = json.dumps({"method": "call", "tool": tool, "params": params}) + "\n"; out, err = proc.communicate(req, timeout=self.call_timeout)
            if proc.returncode not in (0, None): raise RuntimeError(f"stdio server exit {proc.returncode}: {err}")
            resp = json.loads(out.strip().splitlines()[-1]); if not resp.get("ok"): raise RuntimeError(resp.get("error","unknown error")); return resp["result"], key
        raise ValueError(f"unknown server_id: {server_id}")

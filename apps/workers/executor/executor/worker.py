import time as _time
from prometheus_client import Counter, Histogram, start_http_server
MCP_CALLS = Counter("mcp_calls_total", "Total MCP calls", ["server","tool","status"])
MCP_LAT = Histogram("mcp_call_duration_seconds", "MCP call latency", ["server","tool"])
def run():
    try: start_http_server(9100)
    except Exception as e: print(f"[metrics] expose failed: {e}")
    for _ in range(3): _time.sleep(1)
    print("Executor worker bootstrap")
if __name__ == "__main__": run()

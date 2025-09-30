from fastapi import FastAPI
from starlette.responses import Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
app = FastAPI(title="MCP Registry")
POOL_SIZE = Gauge("mcp_stdio_pool_size","Warm-pool size",["server"])
POOL_BUSY = Gauge("mcp_stdio_pool_busy","Warm-pool busy workers",["server"])
POOL_SPAWNS = Gauge("mcp_stdio_spawns_total","Total spawns (counter-like gauge)",["server"])
CB_OPEN = Gauge("mcp_registry_circuit_open","Registry-level circuit open",["server"])
@app.get("/metrics") def metrics(): return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

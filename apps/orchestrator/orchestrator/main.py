from fastapi import FastAPI, Request
from starlette.responses import Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from orchestrator.api import goals

app = FastAPI(title="HTN Orchestrator")
REQS = Counter("http_requests_total", "Total HTTP requests", ["path","method"])

@app.middleware("http")
async def count_requests(request: Request, call_next):
    response = await call_next(request)
    try: REQS.labels(path=request.url.path, method=request.method).inc()
    except Exception: pass
    return response

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/metrics")
def metrics(): return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(goals.router)

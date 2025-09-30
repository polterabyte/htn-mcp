from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="MCP HTTP")

TOOLS = {
    "sum": {
        "inputs": {"numbers": {"type": "array", "items": {"type": "number"}}},
        "outputs": {"sum": {"type": "number"}},
        "version": "1.0",
    },
    "echo": {
        "inputs": {"text": {"type": "string"}},
        "outputs": {"text": {"type": "string"}},
        "version": "1.0",
    },
}

class CallReq(BaseModel):
    params: Dict[str, Any]

@app.get("/tools.list")
def tools_list():
    return {"tools": [{"name": k, **v} for k, v in TOOLS.items()]}

@app.post("/call/{tool}")
def call_tool(tool: str, req: CallReq):
    if tool not in TOOLS:
        raise HTTPException(404, "tool not found")
    if tool == "sum":
        nums = req.params.get("numbers", [])
        if not isinstance(nums, list):
            raise HTTPException(400, "numbers must be list")
        return {"sum": sum(nums)}
    if tool == "echo":
        return {"text": str(req.params.get("text", ""))}
    raise HTTPException(400, "unsupported tool")

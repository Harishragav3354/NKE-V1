from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from mutator.test_runner import run_code
from nke_core.artifact import build_artifact

app = FastAPI(title="Negative Knowledge Engine v1")


class AnalyzeRequest(BaseModel):
    code: str
    context: Dict[str, Any]


@app.get("/health")
def health():
    return {"status": "ok", "message": "NKE backend is running"}


@app.post("/analyze")
def analyze(payload: AnalyzeRequest):
    error = run_code(payload.code)
    artifact = build_artifact(payload.code, error, payload.context)

    if error == "NO_ERROR":
        decision = "UNKNOWN"
    else:
        decision = "REJECTED"

    return {
        "decision": decision,
        "error": error,
        "artifact": artifact,
        "context": payload.context
    }
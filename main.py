from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from nke_query import analyze_failure

# Initialize FastAPI
app = FastAPI(
    title="Negative Knowledge Engine (NKE)",
    description="Epistemic exclusion engine. Memory of known failures.",
    version="1.0.0"
)

# --- Schemas ---

class AnalyzeRequest(BaseModel):
    code: str
    error_type: str
    error_message: str
    assignment_id: str

class MatchResult(BaseModel):
    id: int
    assignment_id: str
    error_type: str
    error_message: str
    distance: float

class AnalyzeResponse(BaseModel):
    decision: str
    nearest_distance: Optional[float]
    top_matches: List[MatchResult]

# --- Endpoints ---

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_endpoint(request: AnalyzeRequest):
    """
    Evaluates a failure artifact against the negative knowledge boundary.
    Outputs REJECTED if within threshold of known failures, otherwise UNKNOWN.
    """
    try:
        # Pass data to our refactored core logic
        result = analyze_failure(
            code=request.code,
            error_type=request.error_type,
            error_message=request.error_message,
            assignment_id=request.assignment_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
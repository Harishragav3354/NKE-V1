from fastapi import FastAPI

app = FastAPI(title="Negative Knowledge Engine v1")


@app.get("/health")
def health():
    return {"status": "ok", "message": "NKE backend is running"}
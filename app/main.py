from fastapi import FastAPI
from app.services.fx_service import get_summary

app = FastAPI(title="FX Summary Service")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/summary")
async def summary(start: str, end: str, breakdown: str = "none"):
    return await get_summary(start, end, breakdown)
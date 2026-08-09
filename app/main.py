from fastapi import FastAPI
from app.db import init_db
from app.routes.ingest import router as ingest_router
from app.routes.resources import router as resources_router
from app.routes.recommendations import router as recommendations_router

app = FastAPI(
    title="Cloud Cost Optimizer & Recommendation Engine",
    version="1.0.0",
    description="FinOps API for AWS/Azure billing analysis and safe decommission recommendations.",
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(ingest_router)
app.include_router(resources_router)
app.include_router(recommendations_router)

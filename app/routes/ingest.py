import os
import tempfile
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.ingestion import ingest

router = APIRouter(prefix="/api/v1/ingest", tags=["ingestion"])

@router.post("/billing")
async def upload_billing(file: UploadFile = File(...), db: Session = Depends(get_db)):
    suffix = os.path.splitext(file.filename or "")[1].lower()
    if suffix not in {".csv", ".json"}:
        raise HTTPException(status_code=400, detail="Upload CSV or JSON.")
    content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        path = tmp.name
    try:
        count = ingest(path, db)
        return {"message": "Billing export ingested", "resources_created": count}
    finally:
        os.unlink(path)

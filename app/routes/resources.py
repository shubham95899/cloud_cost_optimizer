from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Resource
from app.schemas import ResourceOut

router = APIRouter(prefix="/api/v1/resources", tags=["resources"])

@router.get("", response_model=list[ResourceOut])
def list_resources(db: Session = Depends(get_db)):
    return db.query(Resource).order_by(Resource.monthly_cost.desc()).all()

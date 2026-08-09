from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Resource, Recommendation
from app.schemas import AnalyzeResponse, RecommendationOut
from app.services.analyzer import analyze

router = APIRouter(prefix="/api/v1/recommendations", tags=["recommendations"])

@router.post("/analyze", response_model=AnalyzeResponse)
def run_analysis(db: Session = Depends(get_db)):
    resources = db.query(Resource).all()
    recs = analyze(resources, db)
    savings = sum(r.estimated_monthly_savings for r in recs)
    return {
        "resources_analyzed": len(resources),
        "recommendations_created": len(recs),
        "estimated_monthly_savings": savings,
    }

@router.get("", response_model=list[RecommendationOut])
def list_recommendations(db: Session = Depends(get_db)):
    return db.query(Recommendation).order_by(Recommendation.estimated_monthly_savings.desc()).all()

@router.get("/{recommendation_id}", response_model=RecommendationOut)
def get_recommendation(recommendation_id: int, db: Session = Depends(get_db)):
    rec = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return rec

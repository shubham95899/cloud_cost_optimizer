from typing import Optional, List
from pydantic import BaseModel

class ResourceOut(BaseModel):
    id: int
    provider: str
    account_id: Optional[str] = None
    region: Optional[str] = None
    resource_id: str
    resource_type: str
    resource_name: Optional[str] = None
    status: Optional[str] = None
    monthly_cost: float
    currency: str
    cpu_avg_pct: Optional[float] = None
    days_idle: Optional[int] = None
    attached_to: Optional[str] = None

    class Config:
        from_attributes = True

class RecommendationOut(BaseModel):
    id: int
    resource_id: int
    category: str
    severity: str
    reason: str
    estimated_monthly_savings: float
    recommendation: str
    cli_command: Optional[str] = None
    api_logic: Optional[str] = None
    approval_required: bool

    class Config:
        from_attributes = True

class AnalyzeResponse(BaseModel):
    resources_analyzed: int
    recommendations_created: int
    estimated_monthly_savings: float

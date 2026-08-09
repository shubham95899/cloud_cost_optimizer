from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean

from app.db import Base

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    provider = Column(String(20), nullable=False, index=True)
    account_id = Column(String(100), nullable=True, index=True)
    region = Column(String(100), nullable=True)
    resource_id = Column(String(255), nullable=False, index=True)
    resource_type = Column(String(100), nullable=False)
    resource_name = Column(String(255), nullable=True)
    status = Column(String(100), nullable=True)
    monthly_cost = Column(Float, default=0.0)
    currency = Column(String(10), default="USD")
    cpu_avg_pct = Column(Float, nullable=True)
    days_idle = Column(Integer, nullable=True)
    attached_to = Column(String(255), nullable=True)
    tags_json = Column(Text, nullable=True)
    source_file = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, nullable=False, index=True)
    category = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
    reason = Column(Text, nullable=False)
    estimated_monthly_savings = Column(Float, default=0.0)
    recommendation = Column(Text, nullable=False)
    cli_command = Column(Text, nullable=True)
    api_logic = Column(Text, nullable=True)
    approval_required = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

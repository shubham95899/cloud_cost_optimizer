from types import SimpleNamespace
from app.services.recommender import build_recommendations

def test_orphaned_disk():
    r = SimpleNamespace(
        provider="aws", resource_id="vol-1", resource_type="ebs",
        status="unattached", attached_to=None, monthly_cost=10,
        currency="USD", cpu_avg_pct=None, days_idle=None
    )
    result = build_recommendations([r])
    assert result[0]["category"] == "orphaned_storage"
    assert result[0]["savings"] == 10

def test_idle_vm():
    r = SimpleNamespace(
        provider="aws", resource_id="i-1", resource_type="ec2",
        status="running", attached_to=None, monthly_cost=100,
        currency="USD", cpu_avg_pct=2, days_idle=10
    )
    result = build_recommendations([r])
    assert result[0]["category"] == "idle_compute"

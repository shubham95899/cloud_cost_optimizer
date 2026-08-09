from app.models import Resource
from app.config import DEFAULT_IDLE_CPU_PCT, DEFAULT_IDLE_DAYS

def _is_true(value):
    return str(value).lower() in {"true", "yes", "y", "1", "unattached", "orphaned", "idle", "stopped"}

def build_recommendations(resources):
    output = []
    for r in resources:
        rt = (r.resource_type or "").lower()
        status = (r.status or "").lower()
        reason = None
        category = None
        severity = "medium"

        # Disk/storage waste
        if rt in {"ebs", "ebs_volume", "managed_disk", "disk", "azure_disk"}:
            unattached = (not r.attached_to) or _is_true(status) or status in {"unattached", "orphaned"}
            if unattached:
                category = "orphaned_storage"
                severity = "high"
                reason = f"Storage {r.resource_id} is unattached/orphaned and costs {r.monthly_cost:.2f} {r.currency}/month."

        # Idle compute
        elif rt in {"ec2", "ec2_instance", "vm", "azure_vm", "virtual_machine"}:
            cpu = r.cpu_avg_pct
            idle_days = r.days_idle or 0
            if (cpu is not None and cpu < DEFAULT_IDLE_CPU_PCT) and idle_days >= DEFAULT_IDLE_DAYS:
                category = "idle_compute"
                severity = "high" if r.monthly_cost >= 50 else "medium"
                reason = (
                    f"Average CPU is {cpu:.1f}% for {idle_days} idle days; "
                    f"estimated cost is {r.monthly_cost:.2f} {r.currency}/month."
                )
            elif status in {"stopped", "deallocated"} and r.monthly_cost > 0:
                category = "stopped_compute"
                severity = "medium"
                reason = f"Compute resource is {status} but still has associated monthly cost."

        if category:
            output.append({
                "resource": r,
                "category": category,
                "severity": severity,
                "reason": reason,
                "savings": r.monthly_cost,
            })
    return output

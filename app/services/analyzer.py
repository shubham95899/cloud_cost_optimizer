from app.models import Recommendation
from app.services.recommender import build_recommendations
from app.services.command_generator import generate_action

def analyze(resources, db):
    candidates = build_recommendations(resources)
    created = []
    for item in candidates:
        r = item["resource"]
        cli, api = generate_action(r, item["category"])
        rec = Recommendation(
            resource_id=r.id,
            category=item["category"],
            severity=item["severity"],
            reason=item["reason"],
            estimated_monthly_savings=item["savings"],
            recommendation="Review ownership/tags, backup requirements and dependency impact, then decommission if approved.",
            cli_command=cli,
            api_logic=api,
            approval_required=True,
        )
        db.add(rec)
        created.append(rec)
    db.commit()
    return created

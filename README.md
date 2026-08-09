# Cloud Cost Optimizer & Recommendation Engine

A Python, API-first FinOps application that ingests AWS/Azure billing exports in CSV/JSON, detects cost waste such as orphaned storage and idle compute, estimates savings, and generates provider-specific CLI/API decommission logic.

## Important architecture point

Billing exports tell us **what is costing money**. They do not always prove that a resource is currently unattached or idle.

For production, use:
1. Billing export -> cost and resource identifiers.
2. Cloud inventory/metrics -> attachment state, VM state and CPU utilization.
3. Rule engine -> recommendation.
4. Approval workflow -> human review.
5. Command/API generator -> safe decommission action.

This demo accepts those inventory fields in the CSV/JSON so it can run locally without cloud credentials.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger:
http://127.0.0.1:8000/docs

SQLite database `cost_optimizer.db` is automatically created on application startup.

## Test the sample AWS file

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/ingest/billing"   -H "accept: application/json"   -H "Content-Type: multipart/form-data"   -F "file=@sample_data/aws_billing.csv"

curl -X POST "http://127.0.0.1:8000/api/v1/recommendations/analyze"

curl "http://127.0.0.1:8000/api/v1/recommendations"
```

Example recommendation:
- orphaned EBS volume -> `aws ec2 delete-volume --volume-id vol-001 --region ap-south-1`
- idle EC2 -> `aws ec2 terminate-instances --instance-ids i-001 --region ap-south-1`

The application **does not execute these commands**. They are generated as reviewable actions.

## Database

SQLite is used because it is free and zero-configuration.

Tables:
- `resources`: normalized billing/inventory resources
- `recommendations`: detected waste and generated remediation logic

For PostgreSQL, change:
```text
DATABASE_URL=postgresql+psycopg://user:password@host/dbname
```
and add the PostgreSQL driver.

## API

- `GET /health`
- `POST /api/v1/ingest/billing`
- `GET /api/v1/resources`
- `POST /api/v1/recommendations/analyze`
- `GET /api/v1/recommendations`
- `GET /api/v1/recommendations/{id}`

## Recommendation rules

### Orphaned storage
If:
- EBS/managed disk type
- no attachment OR status says unattached/orphaned

then recommend deletion after approval.

### Idle compute
If:
- EC2/VM
- average CPU < 10%
- idle for >= 7 days

then recommend shutdown/termination after dependency and owner checks.

### Savings
For a simple first version:
`estimated_monthly_savings = current_monthly_cost`

A production version should model:
- committed-use/reserved discounts
- storage snapshots
- egress
- minimum billing periods
- termination date
- taxes
- confidence interval

## Production extensions

- AWS Cost & Usage Report (CUR) ingestion from S3
- Azure Cost Management export ingestion
- AWS Resource Groups / EC2 / EBS inventory
- Azure Resource Graph + Compute APIs
- CloudWatch/Azure Monitor CPU metrics
- S3/object storage for raw exports
- PostgreSQL
- authentication/RBAC
- approval/audit workflow
- Slack/Teams notifications
- scheduled jobs
- policy-as-code
- dashboard with savings by account/team/region
- anomaly detection and forecasting
- dry-run mode and two-person approval for destructive actions

## Interview explanation

"I built a Python FastAPI FinOps service that normalizes AWS and Azure billing exports into SQLite, applies rule-based waste detection for orphaned storage and idle compute, calculates estimated savings, and generates provider-specific CLI/API remediation logic. I deliberately separated recommendation from execution so the platform remains safe and auditable. In production, billing data is combined with resource inventory and monitoring metrics because billing alone cannot prove attachment or utilization state."

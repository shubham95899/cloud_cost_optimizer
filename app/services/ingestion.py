import json
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session
from app.models import Resource

REQUIRED_COLUMNS = {"provider", "resource_id", "resource_type", "monthly_cost"}

def _normalise(row: dict, source_file: str) -> dict:
    tags = row.get("tags", row.get("tags_json", {}))
    if not isinstance(tags, str):
        tags = json.dumps(tags)
    return {
        "provider": str(row.get("provider", "")).lower(),
        "account_id": row.get("account_id"),
        "region": row.get("region"),
        "resource_id": str(row.get("resource_id")),
        "resource_type": str(row.get("resource_type", "")).lower(),
        "resource_name": row.get("resource_name"),
        "status": row.get("status"),
        "monthly_cost": float(row.get("monthly_cost", 0) or 0),
        "currency": row.get("currency", "USD"),
        "cpu_avg_pct": float(row["cpu_avg_pct"]) if row.get("cpu_avg_pct") not in (None, "") else None,
        "days_idle": int(row["days_idle"]) if row.get("days_idle") not in (None, "") else None,
        "attached_to": row.get("attached_to"),
        "tags_json": tags,
        "source_file": source_file,
    }

def parse_file(path: str) -> list[dict]:
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(path)
        records = df.to_dict(orient="records")
    elif suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        records = data if isinstance(data, list) else data.get("resources", data.get("data", []))
    else:
        raise ValueError("Only CSV and JSON are supported.")
    if not records:
        return []
    missing = REQUIRED_COLUMNS - set(records[0].keys())
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return [_normalise(r, Path(path).name) for r in records]

def ingest(path: str, db: Session) -> int:
    records = parse_file(path)
    for record in records:
        db.add(Resource(**record))
    db.commit()
    return len(records)

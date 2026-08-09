import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cost_optimizer.db")
RECOMMENDATION_CURRENCY = os.getenv("RECOMMENDATION_CURRENCY", "USD")
DEFAULT_IDLE_CPU_PCT = float(os.getenv("DEFAULT_IDLE_CPU_PCT", "10"))
DEFAULT_IDLE_DAYS = int(os.getenv("DEFAULT_IDLE_DAYS", "7"))

from app.db import engine, init_db
from app.models import Resource, Recommendation

if __name__ == "__main__":
    Resource.metadata.drop_all(bind=engine)
    Recommendation.metadata.drop_all(bind=engine)
    init_db()
    print("Database reset.")

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_PATH = Path(__file__).resolve().parent.parent / "app.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(
 DATABASE_URL,
 connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(
 bind=engine,
 autoflush=False,
 expire_on_commit=False,
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
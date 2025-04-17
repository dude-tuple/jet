__all__ = [
    'get_db',
    'Base'
]

import os
from typing import Any, Generator

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(os.getenv("DATABASE_URL"), echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

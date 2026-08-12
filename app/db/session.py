from collections.abc import Generator
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.exceptions import DatabaseException


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@contextmanager
def transaction(db: Session) -> Iterator[Session]:
    try:
        yield db
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise DatabaseException(
            "Database operation failed.",
        ) from exc
    except Exception:
        db.rollback()
        raise

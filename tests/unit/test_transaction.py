import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import DatabaseException
from app.db.session import transaction


class FakeSession:
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    def commit(self) -> None:
        self.committed = True
        raise SQLAlchemyError("test database error")

    def rollback(self) -> None:
        self.rolled_back = True


def test_transaction_rolls_back_on_database_error() -> None:
    db = FakeSession()

    with pytest.raises(DatabaseException):
        with transaction(db):
            pass

    assert db.committed is True
    assert db.rolled_back is True

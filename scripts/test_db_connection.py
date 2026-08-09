from sqlalchemy import text

from app.db.session import engine


def main() -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection: OK")
        print("SELECT 1 result:", result.scalar())


if __name__ == "__main__":
    main()

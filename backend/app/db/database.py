import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://bizadmin:bizpass123@localhost:5432/ai_business_os"
)

# Create the database connection engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Used by FastAPI routes that need a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_query(sql: str, params: dict = None) -> list:
    """
    Run any SQL query and return results as a list of dictionaries.
    
    Example:
        results = run_query("SELECT * FROM invoices WHERE status = :s", {"s": "unpaid"})
        # returns: [{"id": "...", "status": "unpaid", ...}, ...]
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        columns = list(result.keys())
        rows = result.fetchall()
        return [dict(zip(columns, row)) for row in rows]

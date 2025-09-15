from app.database import engine
from sqlalchemy import text

def test_engine_connects():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT 1"))
        # SQLite y Postgres devuelven 1 para "SELECT 1"
        assert res.scalar() == 1

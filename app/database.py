from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    # necesario para SQLite en apps con múltiples hilos (FastAPI dev)
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
Base = declarative_base()

# Dependency para rutas (cuando implementemos modelos/routers)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

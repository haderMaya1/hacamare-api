import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db

# Base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear todas las tablas antes de los tests
Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    """Crea una sesión de base de datos nueva para cada test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

# Override para que FastAPI use esta sesión en lugar de la real
@pytest.fixture(autouse=True)
def override_get_db(db_session, monkeypatch):
    def _get_db():
        try:
            yield db_session
        finally:
            pass
    monkeypatch.setattr("app.database.get_db", _get_db)
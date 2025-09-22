import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from fastapi.testclient import TestClient
from app.main import app
from app.models import (usuario,password_reset,comentario,contacto,
                        faq,interes,mensaje,notificacion,pais,publicacion,reaccion_publicacion,
                        rol,sesion_chat,solicitud_amistad,usuario_interes,usuario_sesion_chat)
from app.models.rol import Rol
from app.models.pais import Pais
import os

# Detectar DB para tests (por defecto SQLite en memoria)
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")

# Crear engine compartido
if TEST_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(TEST_DATABASE_URL, echo=False)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear todas las tablas al inicio de la sesión de tests
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    # Seeder: rol por defecto
    session = TestingSessionLocal()
    if not session.query(Rol).filter_by(id_rol=1).first():
        session.add(Rol(id_rol=1, nombre="Default", permisos="{}"))
        
    if not session.query(Pais).filter_by(id_pais=1).first():
        session.add(Pais(id_pais=1, pais="Colombia",
                         estado="Antioquia", ciudad="Medellín"))
         
    session.commit()
    session.close()

    yield
    Base.metadata.drop_all(bind=engine)


# Fixture para manejar la sesión (rollback en cada test)
@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

# Fixture para cliente FastAPI que use la misma sesión
@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session  # no cerramos aquí, rollback lo maneja db_session
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
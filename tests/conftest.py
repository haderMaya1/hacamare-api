import pytest
from app.utils.security import hash_password
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from fastapi.testclient import TestClient
from app.main import app
from app.models import (usuario,password_reset, token_blacklist, comentario,contacto,
                        faq,interes,mensaje,notificacion,pais,publicacion,reaccion_publicacion,
                        rol,sesion_chat,solicitud_amistad,usuario_interes,usuario_sesion_chat)
from app.models.rol import Rol
from app.models.pais import Pais
from app.models.usuario import Usuario
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

@pytest.fixture
def admin_token(client, db_session):
    # 1) Asegurar que exista el rol 'Administrador' (case-insensitive)
    rol = db_session.query(Rol).filter(Rol.nombre.ilike("administrador")).first()
    if not rol:
        rol = Rol(nombre="Administrador", permisos='{"all": true}')
        db_session.add(rol)
        db_session.commit()
        db_session.refresh(rol)

    # 2) Crear admin user si no existe
    username = "admin_test"
    admin = db_session.query(Usuario).filter_by(nombre_usuario=username).first()
    if not admin:
        admin = Usuario(
            nombre_usuario=username,
            contraseña=hash_password("admin123"),
            nombres="Admin",
            apellidos="Test",
            edad=30,
            email="admin_test@example.com",
            id_rol=rol.id_rol,
            estado_cuenta="activo",
            email_verificado=True
        )
        db_session.add(admin)
        db_session.commit()
        db_session.refresh(admin)

    # 3) Login vía endpoint para obtener token (asegura que endpoint funcione)
    r = client.post("/auth/login", data={"username": username, "password": "admin123"})
    assert r.status_code == 200, f"Login admin falló: {r.status_code} - {r.text}"
    return r.json()["access_token"]

@pytest.fixture
def user_token(client):
    """Helper para obtener un token válido"""
    client.post("/auth/register", json={
        "nombre_usuario": "pubuser",
        "contraseña": "123456",
        "nombres": "Pub",
        "apellidos": "User",
        "edad": 20,
        "email": "pubuser@example.com",
        "id_rol": 1
    })
    response = client.post("/auth/login", data={"username": "pubuser", "password": "123456"})
    return response.json()["access_token"]
   
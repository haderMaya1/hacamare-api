from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.services.auth_service import register_user, login_user
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea una nueva cuenta de usuario con rol por defecto 'usuario'."
)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return register_user(db, usuario)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Inicio de sesión",
    description="Retorna un token JWT válido para el usuario."
)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    return login_user(db, form_data.username, form_data.password)


@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Usuario autenticado",
    description="Obtiene la información del usuario actual a partir del token."
)
def read_users_me(current_user: UsuarioResponse = Depends(get_current_user)):
    return current_user

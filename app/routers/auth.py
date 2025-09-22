from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.services.auth_service import (register_user, login_user,
                                       refresh_access_token, register_user_admin,
                                       change_password, logout_user)
from app.models.usuario import Usuario
from app.schemas.token_blacklist import RefreshTokenRequest
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, ChangePasswordRequest
from app.utils.security import get_current_user, require_role, get_token_jti

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
    "/registerAdmin",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario administrador",
    description="Crea una nueva cuenta de usuario con rol administrador."
)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db), current_user = Depends(require_role(["admin"]))):
    return register_user_admin(db, usuario)

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

@router.post("/refresh", summary="Renovar Acces Token")
def refresh(body: RefreshTokenRequest, db: Session = Depends(get_db)):
    #Recibe un refres_token cálido y retorna un nuevo access_token.
    return refresh_access_token(db, body.refresh_token)
    
@router.post("/change-password", summary="Cambiar contraseña")
def change_password_route(
    body: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    change_password(db, current_user, body.old_password, body.new_password)
    return {"message": "Contraseña actualizada correctamente"}

@router.post("/logout", summary="Cerrar sesión (revocar token)")
def logout(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    token_jti: str = Depends(get_token_jti)  # helper que extrae jti del JWT
):
    return logout_user(db, token_jti)

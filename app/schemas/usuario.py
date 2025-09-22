from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from app.schemas.interes import InteresResponse


class UsuarioBase(BaseModel):
    nombre_usuario: str
    nombres: str
    apellidos: str
    edad: int
    email: EmailStr
    telefono: Optional[str] = None
    id_pais: Optional[int] = None
    foto_perfil: Optional[str] = None
    id_rol: Optional[int] = None


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    edad: Optional[int] = None
    telefono: Optional[str] = None
    id_pais: Optional[int] = None
    foto_perfil: Optional[str] = None
    estado_cuenta: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    
class UsuarioResponse(UsuarioBase):
    id_usuario: int
    fecha_registro: datetime
    estado_cuenta: str
    email_verificado: bool
    intereses: List[InteresResponse] = []

    class Config:
        orm_mode = True

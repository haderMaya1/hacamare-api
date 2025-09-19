from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UsuarioBase(BaseModel):
    nombre_usuario: str
    nombres: str
    apellidos: str
    edad: int
    email: EmailStr
    telefono: Optional[str] = None
    pais: Optional[str] = None
    estado: Optional[str] = None
    ciudad: Optional[str] = None
    foto_perfil: Optional[str] = None
    id_rol: int


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    edad: Optional[int] = None
    telefono: Optional[str] = None
    pais: Optional[str] = None
    estado: Optional[str] = None
    ciudad: Optional[str] = None
    foto_perfil: Optional[str] = None
    estado_cuenta: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: int
    fecha_registro: datetime
    estado_cuenta: str
    email_verificado: bool

    class Config:
        orm_mode = True

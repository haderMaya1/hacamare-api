from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre_usuario: str = Field(..., max_length=50)
    nombres: str
    apellidos: str
    edad: int = Field(..., ge=13)
    email: EmailStr
    telefono: Optional[str] = None
    pais: Optional[str] = None
    estado: Optional[str] = None
    ciudad: Optional[str] = None
    foto_perfil: Optional[str] = None
    estado_cuenta: Optional[str] = "activo"
    email_verificado: Optional[bool] = False
    id_rol: int

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    edad: Optional[int] = Field(None, ge=13)
    telefono: Optional[str] = None
    pais: Optional[str] = None
    estado: Optional[str] = None
    ciudad: Optional[str] = None
    foto_perfil: Optional[str] = None
    estado_cuenta: Optional[str] = None
    email_verificado: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    fecha_registro: datetime

    class Config:
        from_attributes = True  # en vez de orm_mode

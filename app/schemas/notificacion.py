from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificacionBase(BaseModel):
    tipo: str
    contenido: str
    estado: Optional[str] = "activa"
    id_usuario: int
    id_publicacion: Optional[int] = None
    id_sesion: Optional[int] = None
    id_administrador: Optional[int] = None

class NotificacionCreate(NotificacionBase):
    pass

class NotificacionUpdate(BaseModel):
    tipo: Optional[str] = None
    contenido: Optional[str] = None
    estado: Optional[str] = None

class NotificacionResponse(NotificacionBase):
    id_notificacion: int
    fecha: datetime

    class Config:
        orm_mode = True
        from_attributes = True

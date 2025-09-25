from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SesionChatBase(BaseModel):
    nombre_tema: str
    tipo: Optional[str] = None
    estado: str = "activa"

class SesionChatCreate(SesionChatBase):
    pass

class SesionChatUpdate(BaseModel):
    nombre_tema: Optional[str] = None
    tipo: Optional[str] = None
    estado: Optional[str] = None

class SesionChatResponse(SesionChatBase):
    id_sesion: int
    fecha_creacion: datetime
    anfitrion_id: int

    class Config:
        from_attributes = True
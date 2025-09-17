from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SesionChatBase(BaseModel):
    nombre_tema: str
    tipo: Optional[str] = "público"
    estado: Optional[str] = "activa"
    anfitrion_id: int

class SesionChatCreate(SesionChatBase):
    pass

class SesionChatUpdate(BaseModel):
    nombre_tema: Optional[str] = None
    tipo: Optional[str] = None
    estado: Optional[str] = None

class SesionChatResponse(SesionChatBase):
    id_sesion: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True

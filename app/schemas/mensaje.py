from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MensajeBase(BaseModel):
    contenido: str
    imagen: Optional[str] = None

class MensajeCreate(MensajeBase):
    id_sesion: int

class MensajeUpdate(BaseModel):
    contenido: Optional[str] = None
    imagen: Optional[str] = None

class MensajeResponse(MensajeBase):
    id_mensaje: int
    fecha_envio: datetime
    id_remitente: int
    id_sesion: int

    class Config:
        from_attributes = True
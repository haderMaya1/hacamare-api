from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MensajeBase(BaseModel):
    contenido: str
    imagen: Optional[str] = None
    id_remitente: int
    id_sesion: int

class MensajeCreate(MensajeBase):
    pass

class MensajeResponse(MensajeBase):
    id_mensaje: int
    fecha_envio: datetime

    class Config:
        orm_mode = True

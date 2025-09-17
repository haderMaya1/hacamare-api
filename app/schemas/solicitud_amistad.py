from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SolicitudBase(BaseModel):
    mensaje: Optional[str] = None
    remitente_id: int
    destinatario_id: int

class SolicitudCreate(SolicitudBase):
    pass

class SolicitudResponse(SolicitudBase):
    id_solicitud: int
    estado: str
    fecha_envio: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SolicitudBase(BaseModel):
    destinatario_id: int
    mensaje: Optional[str] = None

class SolicitudCreate(SolicitudBase):
    pass

class SolicitudUpdate(BaseModel):
    estado: str  # "aceptada" o "rechazada"

class SolicitudResponse(BaseModel):
    id_solicitud: int
    mensaje: Optional[str]
    estado: str
    fecha_envio: datetime
    remitente_id: int
    destinatario_id: int

    class Config:
        orm_mode = True
        from_attributes = True

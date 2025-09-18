from pydantic import BaseModel
from datetime import datetime

class SolicitudAmistadBase(BaseModel):
    mensaje: str | None = None
    estado: str | None = "pendiente"

class SolicitudAmistadCreate(SolicitudAmistadBase):
    remitente_id: int
    destinatario_id: int

class SolicitudAmistadUpdate(BaseModel):
    mensaje: str | None = None
    estado: str | None = None

class SolicitudAmistadResponse(SolicitudAmistadBase):
    id_solicitud: int
    remitente_id: int
    destinatario_id: int
    fecha_envio: datetime

    class Config:
        from_attributes = True

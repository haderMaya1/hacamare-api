from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class SolicitudAmistad(Base):
    __tablename__ = "solicitud_amistad"

    id_solicitud = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mensaje = Column(Text, nullable=True)
    estado = Column(String, CheckConstraint("estado IN ('pendiente', 'aceptada', 'rechazada')"), default="pendiente")
    fecha_envio = Column(DateTime, default=datetime.utcnow)
    remitente_id = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    destinatario_id = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)

    remitente = relationship("Usuario", foreign_keys=[remitente_id], back_populates="solicitudes_enviadas")
    destinatario = relationship("Usuario", foreign_keys=[destinatario_id], back_populates="solicitudes_recibidas")

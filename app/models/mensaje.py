from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Mensaje(Base):
    __tablename__ = "mensaje"

    id_mensaje = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text, nullable=False)
    imagen = Column(Text, nullable=True)
    fecha_envio = Column(DateTime(timezone=True), server_default=func.now())

    id_remitente = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_sesion = Column(Integer, ForeignKey("sesion_chat.id_sesion"), nullable=False)

    remitente = relationship("Usuario", back_populates="mensajes")
    sesion = relationship("SesionChat", back_populates="mensajes")

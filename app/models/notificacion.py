from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from app.database import Base

class Notificacion(Base):
    __tablename__ = "notificacion"

    id_notificacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(Text, CheckConstraint("tipo IN ('eliminacion', 'advertencia')"), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha = Column(DateTime, default=func.now())
    estado = Column(Text, CheckConstraint("estado IN ('activa', 'resuelta')"), default="activa")

    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_publicacion = Column(Integer, ForeignKey("publicacion.id_publicacion"), nullable=True)
    id_sesion = Column(Integer, ForeignKey("sesion_chat.id_sesion"), nullable=True)
    id_administrador = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=True)

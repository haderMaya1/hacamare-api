from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base

class SesionChat(Base):
    __tablename__ = "sesion_chat"

    id_sesion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_tema = Column(String, nullable=False)
    tipo = Column(String, CheckConstraint("tipo IN ('privado', 'público')"), default="público")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String, CheckConstraint("estado IN ('activa', 'cerrada', 'eliminada')"), default="activa")
    anfitrion_id = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)

    # Relación con Usuario (anfitrión)
    anfitrion = relationship("Usuario", back_populates="sesiones_chat")
    usuarios = relationship("Usuario", secondary="usuario_sesion_chat", back_populates="sesiones")

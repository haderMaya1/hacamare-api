from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base

class Publicacion(Base):
    __tablename__ = "publicacion"

    id_publicacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    texto = Column(Text, nullable=False)
    imagen = Column(String, nullable=True)
    fecha_publicacion = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String, CheckConstraint("estado IN ('visible', 'oculto', 'eliminado')"), default="visible")
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)

    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="publicaciones")
    reacciones = relationship("ReaccionPublicacion", back_populates="publicacion", cascade="all, delete-orphan")
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Comentario(Base):
    __tablename__ = "comentario"

    id_comentario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, CheckConstraint("estado IN ('visible', 'oculto', 'eliminado')"), default="visible")
    id_publicacion = Column(Integer, ForeignKey("publicacion.id_publicacion", ondelete="CASCADE"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_comentario_padre = Column(Integer, ForeignKey("comentario.id_comentario", ondelete="CASCADE"), nullable=True)
    imagen = Column(String, nullable=True)

    publicacion = relationship("Publicacion", back_populates="comentarios")
    usuario = relationship("Usuario", back_populates="comentarios")
    respuestas = relationship("Comentario", cascade="all, delete", backref="comentario_padre", remote_side=[id_comentario])

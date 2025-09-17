from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ReaccionPublicacion(Base):
    __tablename__ = "reaccion_publicacion"

    id_reaccion = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(
        Text,
        nullable=False
    )
    fecha_reaccion = Column(DateTime, default=datetime.utcnow)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_publicacion = Column(Integer, ForeignKey("publicacion.id_publicacion"), nullable=False)

    usuario = relationship("Usuario", back_populates="reacciones")
    publicacion = relationship("Publicacion", back_populates="reacciones")

    __table_args__ = (CheckConstraint("tipo IN ('like', 'dislike', 'me_encanta', 'me_divierte', 'me_asombra', 'me_entristece', 'me_enoja')",
            name="check_tipo_reaccion"),
    )

from sqlalchemy import Column, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Contacto(Base):
    __tablename__ = "contacto"

    id_contacto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id_1 = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    usuario_id_2 = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    fecha_aceptacion = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("usuario_id_1 != usuario_id_2", name="chk_usuarios_diferentes"),
    )

    usuario1 = relationship("Usuario", foreign_keys=[usuario_id_1], back_populates="contactos1")
    usuario2 = relationship("Usuario", foreign_keys=[usuario_id_2], back_populates="contactos2")

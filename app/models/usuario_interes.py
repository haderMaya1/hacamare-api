from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class UsuarioInteres(Base):
    __tablename__ = "usuario_interes"

    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    id_interes = Column(Integer, ForeignKey("interes.id_interes"), primary_key=True)

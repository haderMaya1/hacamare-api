from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.usuario_interes import UsuarioInteres

class Interes(Base):
    __tablename__ = "interes"

    id_interes = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(100), nullable=True)

    usuarios = relationship("Usuario", secondary=UsuarioInteres, back_populates="intereses")
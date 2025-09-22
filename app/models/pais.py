from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Pais(Base):
    __tablename__ = "pais"

    id_pais = Column(Integer, primary_key=True, index=True)
    pais = Column(String(50), nullable=False)
    estado = Column(String(50), nullable=False)
    ciudad = Column(String(50), nullable=False)

    usuarios = relationship("Usuario", back_populates="pais")

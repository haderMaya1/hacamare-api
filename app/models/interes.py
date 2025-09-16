from sqlalchemy import Column, Integer, String
from app.database import Base

class Interes(Base):
    __tablename__ = "interes"

    id_interes = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(100), nullable=True)

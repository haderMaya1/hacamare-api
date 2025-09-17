from sqlalchemy import Column, Integer, Text
from app.database import Base

class Faq(Base):
    __tablename__ = "faq"

    id_faq = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pregunta = Column(Text, nullable=False)
    respuesta = Column(Text, nullable=False)

from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

class UsuarioSesionChat(Base):
    __tablename__ = "usuario_sesion_chat"

    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), primary_key=True)
    id_sesion = Column(Integer, ForeignKey("sesion_chat.id_sesion"), primary_key=True)

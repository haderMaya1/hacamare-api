from sqlalchemy import Column, Integer, ForeignKey, Table
from app.database import Base

UsuarioSesionChat = Table(
    "usuario_sesion_chat",
    Base.metadata,
    Column("id_usuario", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("id_sesion", Integer, ForeignKey("sesion_chat.id_sesion"), primary_key=True),
)

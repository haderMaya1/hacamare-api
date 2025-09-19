from sqlalchemy import Column, Integer, ForeignKey, Table
from app.database import Base

UsuarioInteres = Table(
    "usuario_interes",
    Base.metadata,
    Column("id_usuario", Integer, ForeignKey("usuario.id_usuario"), primary_key=True),
    Column("id_interes", Integer, ForeignKey("interes.id_interes"), primary_key=True),
)

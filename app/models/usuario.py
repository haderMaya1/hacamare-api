from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20))
    pais = Column(String(50))
    estado = Column(String(50))
    ciudad = Column(String(50))
    foto_perfil = Column(String)  # URL o base64
    fecha_registro = Column(DateTime, server_default=func.now())
    estado_cuenta = Column(String(20), default="activo")
    email_verificado = Column(Boolean, default=False)
    token_verificacion = Column(String(255))
    token_recuperacion = Column(String(255))
    expiracion_token = Column(DateTime)

    id_rol = Column(Integer, ForeignKey("rol.id_rol"), nullable=False)
    rol = relationship("Rol", back_populates="usuarios")
    publicaciones = relationship("Publicacion", back_populates="usuario", cascade="all, delete-orphan")
    sesiones_chat = relationship("SesionChat", back_populates="anfitrion", cascade="all, delete-orphan")
    sesiones = relationship("SesionChat", secondary="usuario_sesion_chat", back_populates="usuarios")
    mensajes = relationship("Mensaje", back_populates="remitente")
    reacciones = relationship("ReaccionPublicacion", back_populates="usuario", cascade="all, delete-orphan")
    comentarios = relationship("Comentario", back_populates="usuario", cascade="all, delete-orphan")
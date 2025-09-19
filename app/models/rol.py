import json
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    permisos = Column(Text, default="{}")  # Guardamos como string JSON

    usuarios = relationship("Usuario", back_populates="rol")

    def set_permisos(self, permisos_dict: dict):
        """Convierte dict → JSON string para guardar en DB"""
        self.permisos = json.dumps(permisos_dict)

    def get_permisos(self) -> dict:
        """Convierte JSON string → dict al leer desde DB"""
        return json.loads(self.permisos or "{}")

    @property
    def permisos_dict(self) -> dict:
        """Propiedad para exponer permisos como dict a Pydantic"""
        return self.get_permisos()
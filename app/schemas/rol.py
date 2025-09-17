from typing import Optional, Dict
from pydantic import BaseModel
import json

class RolBase(BaseModel):
    nombre: str
    permisos: Optional[Dict] = {}

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    permisos: Optional[Dict] = None

class RolOut(BaseModel):
    id_rol: int
    nombre: str
    permisos: dict

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id_rol=obj.id_rol,
            nombre=obj.nombre,
            permisos=obj.get_permisos()  # usamos helper del modelo
        )

class RolResponse(RolBase):
    id_rol: int

    class Config:
        orm_mode = True

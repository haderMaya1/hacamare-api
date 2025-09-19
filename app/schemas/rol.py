from pydantic import BaseModel
from typing import Optional, Dict

class RolBase(BaseModel):
    nombre: str
    permisos: Optional[Dict] = {}

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    permisos: Optional[Dict] = None

class RolResponse(BaseModel):
    id_rol: int
    nombre: str
    permisos_dict: Dict   # usamos la propiedad, no la columna raw

    class Config:
        orm_mode = True
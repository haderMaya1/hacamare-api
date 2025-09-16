from pydantic import BaseModel
from typing import Dict, Optional

class RolBase(BaseModel):
    nombre: str
    permisos: Optional[Dict] = {}

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    permisos: Optional[Dict] = None

class RolResponse(RolBase):
    id_rol: int

    class Config:
        orm_mode = True
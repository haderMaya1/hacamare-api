from pydantic import BaseModel
from typing import Optional, Dict

class RolBase(BaseModel):
    nombre: str
    permisos: Optional[Dict[str, str]] = None  # Dict para representar JSON

    model_config = {"from_attributes": True}  # equivale a orm_mode=True en Pydantic v2

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    permisos: Optional[Dict[str, str]] = None

    model_config = {"from_attributes": True}

class RolResponse(RolBase):
    id_rol: int

    model_config = {"from_attributes": True}

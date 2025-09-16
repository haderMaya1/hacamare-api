from pydantic import BaseModel
from typing import Optional

class InteresBase(BaseModel):
    nombre: str
    categoria: Optional[str] = None

class InteresCreate(InteresBase):
    pass

class InteresUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None

class InteresOut(InteresBase):
    id_interes: int

    class Config:
        from_attributes = True

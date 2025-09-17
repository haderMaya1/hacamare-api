from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PublicacionBase(BaseModel):
    texto: str
    imagen: Optional[str] = None
    estado: Optional[str] = "visible"
    id_usuario: int

class PublicacionCreate(PublicacionBase):
    pass

class PublicacionUpdate(BaseModel):
    texto: Optional[str] = None
    imagen: Optional[str] = None
    estado: Optional[str] = None

class PublicacionResponse(PublicacionBase):
    id_publicacion: int
    fecha_publicacion: datetime

    class Config:
        orm_mode = True

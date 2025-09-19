from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PublicacionBase(BaseModel):
    texto: str
    imagen: Optional[str] = None


class PublicacionCreate(PublicacionBase):
    pass


class PublicacionUpdate(BaseModel):
    texto: Optional[str] = None
    imagen: Optional[str] = None
    estado: Optional[str] = None


class PublicacionResponse(PublicacionBase):
    id_publicacion: int
    fecha_publicacion: datetime
    estado: str
    id_usuario: int

    class Config:
        orm_mode = True

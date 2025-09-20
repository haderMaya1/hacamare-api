from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ComentarioBase(BaseModel):
    contenido: str
    estado: Optional[str] = "visible"
    id_publicacion: int
    id_comentario_padre: Optional[int] = None
    imagen: Optional[str] = None

class ComentarioCreate(ComentarioBase):
    pass
    
class ComentarioUpdate(BaseModel):
    contenido: Optional[str] = None
    estado: Optional[str] = None
    imagen: Optional[str] = None

class ComentarioResponse(BaseModel):
    id_comentario: int
    contenido: str
    fecha_creacion: datetime
    estado: str
    id_publicacion: int
    id_usuario: int
    id_comentario_padre: Optional[int]
    imagen: Optional[str]

    class Config:
        orm_mode = True

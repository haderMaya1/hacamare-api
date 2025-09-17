from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ComentarioBase(BaseModel):
    contenido: str
    id_publicacion: int
    id_usuario: int
    id_comentario_padre: Optional[int] = None
    imagen: Optional[str] = None

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioResponse(ComentarioBase):
    id_comentario: int
    fecha_creacion: datetime
    estado: str

    class Config:
        orm_mode = True

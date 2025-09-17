from pydantic import BaseModel
from datetime import datetime

class ReaccionPublicacionBase(BaseModel):
    tipo: str
    id_usuario: int
    id_publicacion: int

class ReaccionPublicacionCreate(ReaccionPublicacionBase):
    pass

class ReaccionPublicacionUpdate(BaseModel):
    tipo: str

class ReaccionPublicacionResponse(ReaccionPublicacionBase):
    id_reaccion: int
    fecha_reaccion: datetime

    class Config:
        orm_mode = True

    class Config:
        from_attributes = True
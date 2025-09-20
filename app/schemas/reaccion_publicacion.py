from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReaccionBase(BaseModel):
    tipo: str  # like, dislike, me_encanta, etc.
    id_publicacion: int

class ReaccionCreate(ReaccionBase):
    pass

class ReaccionUpdate(BaseModel):
    tipo: Optional[str] = None

class ReaccionResponse(ReaccionBase):
    id_reaccion: int
    fecha_reaccion: datetime
    id_usuario: int

    class Config:
        from_attributes = True

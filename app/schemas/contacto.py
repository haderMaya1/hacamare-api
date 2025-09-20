from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ContactoBase(BaseModel):
    usuario_id_2: int   # ID del usuario con quien se crea el contacto

class ContactoCreate(ContactoBase):
    pass

class ContactoResponse(BaseModel):
    id_contacto: int
    usuario_id_1: int
    usuario_id_2: int
    fecha_aceptacion: datetime

    class Config:
        orm_mode = True
        from_attributes = True

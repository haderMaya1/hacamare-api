from pydantic import BaseModel
from datetime import datetime

class ContactoBase(BaseModel):
    usuario_id_1: int
    usuario_id_2: int

class ContactoCreate(ContactoBase):
    pass

class ContactoResponse(ContactoBase):
    id_contacto: int
    fecha_aceptacion: datetime

    class Config:
        orm_mode = True

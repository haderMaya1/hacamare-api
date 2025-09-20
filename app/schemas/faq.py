from pydantic import BaseModel
from typing import Optional

class FaqBase(BaseModel):
    pregunta: str
    respuesta: str

class FaqCreate(FaqBase):
    pass

class FaqUpdate(BaseModel):
    pregunta: Optional[str] = None
    respuesta: Optional[str] = None

class FaqResponse(FaqBase):
    id_faq: int

    class Config:
        orm_mode = True
        from_attributes = True

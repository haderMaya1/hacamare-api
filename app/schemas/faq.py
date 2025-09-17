from pydantic import BaseModel

class FaqBase(BaseModel):
    pregunta: str
    respuesta: str

class FaqCreate(FaqBase):
    pass

class FaqUpdate(FaqBase):
    pass

class FaqResponse(FaqBase):
    id_faq: int

    class Config:
        orm_mode = True

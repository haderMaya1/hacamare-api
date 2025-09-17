from pydantic import BaseModel

class FaqBase(BaseModel):
    pregunta: str
    respuesta: str

class FaqCreate(FaqBase):
    pass

class FaqUpdate(BaseModel):
    pregunta: str | None = None
    respuesta: str | None = None
    
class FaqResponse(FaqBase):
    id_faq: int

    class Config:
        orm_mode = True
    
    class Config:
        from_attributes = True

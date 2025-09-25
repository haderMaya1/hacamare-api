from pydantic import BaseModel

class PaisBase(BaseModel):
    pais: str
    estado: str
    ciudad: str

class PaisCreate(PaisBase):
    pass

class PaisUpdate(BaseModel):
    pais: str | None = None
    estado: str | None = None
    ciudad: str | None = None

class PaisResponse(PaisBase):
    id_pais: int
    class Config:
        orm_mode = True

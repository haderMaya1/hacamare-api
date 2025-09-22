from pydantic import BaseModel
from typing import Optional

class PaisBase(BaseModel):
    pais: str
    estado: str
    ciudad: str

class PaisCreate(PaisBase):
    pass

class PaisResponse(PaisBase):
    id_pais: int
    
    class Config:
        orm_mode = True

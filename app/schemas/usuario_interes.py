from pydantic import BaseModel

class UsuarioInteresBase(BaseModel):
    id_usuario: int
    id_interes: int

class UsuarioInteresCreate(UsuarioInteresBase):
    pass

class UsuarioInteresResponse(UsuarioInteresBase):
    class Config:
        from_attributes = True

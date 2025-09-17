from pydantic import BaseModel

class UsuarioSesionChatBase(BaseModel):
    id_usuario: int
    id_sesion: int

class UsuarioSesionChatCreate(UsuarioSesionChatBase):
    pass

class UsuarioSesionChatResponse(UsuarioSesionChatBase):
    class Config:
        orm_mode = True

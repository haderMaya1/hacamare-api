from pydantic import BaseModel

class ResetRequest(BaseModel):
    email: str

class ResetConfirm(BaseModel):
    token: str
    new_password: str
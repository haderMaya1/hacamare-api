from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class RevokedToken(Base):
    __tablename__ = "revoked_token"
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True)  # ID único del token
    created_at = Column(DateTime, server_default=func.now())

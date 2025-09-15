from fastapi import FastAPI
from app.config import settings

app = FastAPI(title="Hacamare API - MVP")

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "env": settings.ENV}
from fastapi import FastAPI
from app.config import settings
from app.routers import rol

# Inicialización de la app FastAPI
app = FastAPI(
    title="Hacamare API - MVP",
    description="Backend inicial con manejo de roles",
    version="0.1.0"
)

# Inclusión de routers
app.include_router(rol.router)

# Ruta de healthcheck
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "env": settings.ENV,
        "version": "0.1.0"
    }
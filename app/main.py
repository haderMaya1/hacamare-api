from fastapi import FastAPI
from app.config import settings
from app.routers import rol, usuarios, interes, usuario_interes, publicaciones, sesion_chat, usuario_sesion_chat, mensaje, reaccion_publicacion, comentarios, solicitud_amistad, contactos, faq, notificaciones, auth

# Inicialización de la app FastAPI
app = FastAPI(
    title="Hacamare API - MVP",
    description="Backend inicial con manejo de roles",
    version="0.1.0"
)

# Inclusión de routers
app.include_router(rol.router)
app.include_router(usuarios.router)
app.include_router(interes.router)
app.include_router(usuario_interes.router)
app.include_router(publicaciones.router)
app.include_router(sesion_chat.router)
app.include_router(usuario_sesion_chat.router)
app.include_router(mensaje.router)
app.include_router(reaccion_publicacion.router)
app.include_router(comentarios.router)
app.include_router(solicitud_amistad.router)
app.include_router(contactos.router)
app.include_router(faq.router)
app.include_router(notificaciones.router)
app.include_router(auth.router)

# Ruta de healthcheck
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "env": settings.ENV,
        "version": "0.1.0"
    }
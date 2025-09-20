from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy import insert
from app.database import SessionLocal
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.interes import Interes
from app.models.usuario_interes import UsuarioInteres
from app.models.publicacion import Publicacion
from app.models.sesion_chat import SesionChat
from app.models.usuario_sesion_chat import UsuarioSesionChat
from app.models.mensaje import Mensaje
from app.models.reaccion_publicacion import ReaccionPublicacion
from app.models.comentario import Comentario
from app.models.solicitud_amistad import SolicitudAmistad
from app.models.contacto import Contacto
from app.models.faq import Faq
from app.models.notificacion import Notificacion
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_seed_data():
    db = SessionLocal()
    try:
        # ----------- Roles -----------
        if not db.query(Rol).first():
            admin_rol = Rol(nombre="Administrador", permisos='{"all":true}')
            user_rol = Rol(nombre="Usuario", permisos='{}')
            db.add_all([admin_rol, user_rol])
            db.commit()
        else:
            admin_rol, user_rol = db.query(Rol).all()[:2]

        # ----------- Usuarios -----------
        if not db.query(Usuario).first():
            admin = Usuario(
                nombre_usuario="admin",
                contraseña=pwd_context.hash("admin123"),
                nombres="Admin",
                apellidos="Principal",
                edad=30,
                email="admin@example.com",
                estado_cuenta="activo",
                email_verificado=1,
                id_rol=admin_rol.id_rol
            )
            user1 = Usuario(
                nombre_usuario="juan",
                contraseña=pwd_context.hash("juan123"),
                nombres="Juan",
                apellidos="Pérez",
                edad=25,
                email="juan@example.com",
                estado_cuenta="activo",
                email_verificado=1,
                id_rol=user_rol.id_rol
            )
            user2 = Usuario(
                nombre_usuario="maria",
                contraseña=pwd_context.hash("maria123"),
                nombres="María",
                apellidos="García",
                edad=22,
                email="maria@example.com",
                estado_cuenta="activo",
                email_verificado=1,
                id_rol=user_rol.id_rol
            )
            db.add_all([admin, user1, user2])
            db.commit()
        else:
            admin, user1, user2 = db.query(Usuario).all()[:3]

        # ----------- Intereses -----------
        if not db.query(Interes).first():
            deporte = Interes(nombre="Deporte", categoria="Ocio")
            musica = Interes(nombre="Música", categoria="Arte")
            db.add_all([deporte, musica])
            db.commit()
        else:
            deporte, musica = db.query(Interes).all()[:2]

        # ----------- Usuario_Interes -----------
        if not db.query(UsuarioInteres).first():
            db.execute(
                insert(UsuarioInteres),
                [
                    {"id_usuario": user1.id_usuario, "id_interes": deporte.id_interes},
                    {"id_usuario": user2.id_usuario, "id_interes": musica.id_interes},
                ]
            )
            db.commit()

        # ----------- Publicaciones -----------
        if not db.query(Publicacion).first():
            pub1 = Publicacion(texto="Hola, esta es mi primera publicación",
                               id_usuario=user1.id_usuario, estado="visible")
            pub2 = Publicacion(texto="Escuchando música nueva",
                               id_usuario=user2.id_usuario, estado="visible")
            db.add_all([pub1, pub2])
            db.commit()
        else:
            pub1, pub2 = db.query(Publicacion).all()[:2]

        # ----------- Sesión de chat -----------
        if not db.query(SesionChat).first():
            sesion = SesionChat(
                nombre_tema="Chat General",
                tipo="privado",
                estado="activa",
                anfitrion_id=admin.id_usuario
            )
            db.add(sesion)
            db.commit()
        else:
            sesion = db.query(SesionChat).first()

        # ----------- Usuario_Sesion_Chat -----------
        if not db.query(UsuarioSesionChat).first():
            db.execute(
                insert(UsuarioSesionChat),
                [
                    {"id_usuario": user1.id_usuario, "id_sesion": sesion.id_sesion},
                    {"id_usuario": user2.id_usuario, "id_sesion": sesion.id_sesion},
                ]
            )
            db.commit()

        # ----------- Mensajes -----------
        if not db.query(Mensaje).first():
            db.add_all([
                Mensaje(contenido="Hola a todos!", id_remitente=user1.id_usuario, id_sesion=sesion.id_sesion),
                Mensaje(contenido="Bienvenido!", id_remitente=admin.id_usuario, id_sesion=sesion.id_sesion)
            ])
            db.commit()

        # ----------- Reacciones -----------
        if not db.query(ReaccionPublicacion).first():
            db.add(ReaccionPublicacion(tipo="like", id_usuario=user2.id_usuario, id_publicacion=pub1.id_publicacion))
            db.commit()

        # ----------- Comentarios -----------
        if not db.query(Comentario).first():
            db.add(Comentario(contenido="Buen post!", id_publicacion=pub1.id_publicacion, id_usuario=user2.id_usuario))
            db.commit()

        # ----------- Solicitudes de amistad -----------
        if not db.query(SolicitudAmistad).first():
            db.add(SolicitudAmistad(
                mensaje="¿Quieres ser mi amigo?",
                estado="pendiente",
                remitente_id=user1.id_usuario,
                destinatario_id=user2.id_usuario
            ))
            db.commit()

        # ----------- Contactos -----------
        if not db.query(Contacto).first():
            db.add(Contacto(usuario_id_1=admin.id_usuario, usuario_id_2=user1.id_usuario))
            db.commit()

        # ----------- FAQ -----------
        if not db.query(Faq).first():
            db.add_all([
                Faq(pregunta="¿Cómo registrarse?", respuesta="Haz clic en el botón de registro."),
                Faq(pregunta="¿Cómo recuperar contraseña?", respuesta="Utiliza la opción de recuperar en el login.")
            ])
            db.commit()

        # ----------- Notificaciones -----------
        if not db.query(Notificacion).first():
            db.add(Notificacion(
                tipo="advertencia",
                contenido="Publicación revisada por administrador",
                estado="activa",
                id_usuario=user1.id_usuario,
                id_publicacion=pub1.id_publicacion,
                id_administrador=admin.id_usuario
            ))
            db.commit()

        print("Datos iniciales creados correctamente.")
    finally:
        db.close()


if __name__ == "__main__":
    create_seed_data()

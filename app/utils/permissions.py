"""
Matriz central de permisos.
Las claves de permiso son strings legibles y las rutas piden permisos concretos.
"""

PERMISSIONS = {
    # Administrador: permiso global
    "administrador": {"all": True},

    # Usuario normal: lista mínima de permisos
    "usuario": {
        "auth:login": True,
        "usuarios:read_self": True,
        "usuarios:update_self": True,
        "usuarios:change_password": True,
        "publicaciones:create": True,
        "publicaciones:read_all": True,
        "publicaciones:update_own": True,
        "publicaciones:delete_own": True,
        "comentarios:create": True,
        "comentarios:read": True,
        "solicitudes:create": True,
        "contactos:create": True,
        "faq:read": True,
    },

    # Anónimo: solo lectura pública
    "anonimo": {
        "publicaciones:read_all": True,
        "faq:read": True,
    }
}

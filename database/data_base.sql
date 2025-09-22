-- Tabla rol
CREATE TABLE rol (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    permisos TEXT DEFAULT '{}'
);

CREATE TABLE pais (
    id_pais INTEGER PRIMARY KEY AUTOINCREMENT,
    pais TEXT NOT NULL,
    estado TEXT NOT NULL,
    ciudad TEXT NOT NULL
);

-- Tabla usuario
CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    edad INTEGER CHECK (edad >= 13),
    email TEXT UNIQUE NOT NULL,
    telefono TEXT,
    id_pais INTEGER,
    foto_perfil TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado_cuenta TEXT CHECK (estado_cuenta IN ('activo', 'inactivo', 'bloqueado')),
    email_verificado INTEGER DEFAULT 0,
    token_verificacion TEXT,
    token_recuperacion TEXT,
    expiracion_token DATETIME,
    id_rol INTEGER NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES rol (id_rol) ON DELETE RESTRICT,
    FOREIGN KEY (id_pais) REFERENCES pais (id_pais) ON DELETE SET NULL
);

-- Tabla interes
CREATE TABLE interes (
    id_interes INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT
);

-- Tabla usuario_interes
CREATE TABLE usuario_interes (
    id_usuario INTEGER NOT NULL,
    id_interes INTEGER NOT NULL,
    PRIMARY KEY (id_usuario, id_interes),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_interes) REFERENCES interes (id_interes)
);

-- Tabla publicacion
CREATE TABLE publicacion (
    id_publicacion INTEGER PRIMARY KEY AUTOINCREMENT,
    texto TEXT NOT NULL,
    imagen TEXT,
    fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TEXT CHECK (estado IN ('visible', 'oculto', 'eliminado')),
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);

-- Tabla sesion_chat
CREATE TABLE sesion_chat (
    id_sesion INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_tema TEXT NOT NULL,
    tipo TEXT CHECK (tipo IN ('privado', 'público')),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TEXT CHECK (estado IN ('activa', 'cerrada', 'eliminada')),
    anfitrion_id INTEGER NOT NULL,
    FOREIGN KEY (anfitrion_id) REFERENCES usuario (id_usuario)
);

-- Tabla usuario_sesion_chat
CREATE TABLE usuario_sesion_chat (
    id_usuario INTEGER NOT NULL,
    id_sesion INTEGER NOT NULL,
    PRIMARY KEY (id_usuario, id_sesion),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_sesion) REFERENCES sesion_chat (id_sesion)
);

-- Tabla mensaje
CREATE TABLE mensaje (
    id_mensaje INTEGER PRIMARY KEY AUTOINCREMENT,
    contenido TEXT NOT NULL,
    imagen TEXT,
    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_remitente INTEGER NOT NULL,
    id_sesion INTEGER NOT NULL,
    FOREIGN KEY (id_remitente) REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_sesion) REFERENCES sesion_chat (id_sesion)
);

-- Tabla reaccion_publicacion
CREATE TABLE reaccion_publicacion (
    id_reaccion INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT CHECK (tipo IN ('like', 'dislike', 'me_encanta', 'me_divierte', 'me_asombra', 'me_entristece', 'me_enoja')) NOT NULL,
    fecha_reaccion DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_usuario INTEGER NOT NULL,
    id_publicacion INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_publicacion) REFERENCES publicacion (id_publicacion)
);

-- Tabla comentario
CREATE TABLE comentario (
    id_comentario INTEGER PRIMARY KEY AUTOINCREMENT,
    contenido TEXT NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TEXT CHECK (estado IN ('visible', 'oculto', 'eliminado')) DEFAULT 'visible',
    id_publicacion INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    id_comentario_padre INTEGER,  -- Para comentarios anidados/respuestas
    imagen TEXT,  -- Opcional: para comentarios con imagen
    FOREIGN KEY (id_publicacion) REFERENCES publicacion (id_publicacion) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_comentario_padre) REFERENCES comentario (id_comentario) ON DELETE CASCADE,
    CHECK (id_comentario_padre != id_comentario)  -- Evitar auto-referencia
);

-- Tabla solicitud_amistad
CREATE TABLE solicitud_amistad (
    id_solicitud INTEGER PRIMARY KEY AUTOINCREMENT,
    mensaje TEXT,
    estado TEXT CHECK (estado IN ('pendiente', 'aceptada', 'rechazada')),
    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    remitente_id INTEGER NOT NULL,
    destinatario_id INTEGER NOT NULL,
    FOREIGN KEY (remitente_id) REFERENCES usuario (id_usuario),
    FOREIGN KEY (destinatario_id) REFERENCES usuario (id_usuario),
    CHECK (remitente_id != destinatario_id)
);

-- Tabla contacto
CREATE TABLE contacto (
    id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id_1 INTEGER NOT NULL,
    usuario_id_2 INTEGER NOT NULL,
    fecha_aceptacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id_1) REFERENCES usuario (id_usuario),
    FOREIGN KEY (usuario_id_2) REFERENCES usuario (id_usuario),
    CHECK (usuario_id_1 != usuario_id_2)
);

-- Tabla faq
CREATE TABLE faq (
    id_faq INTEGER PRIMARY KEY AUTOINCREMENT,
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL
);

-- Tabla notificacion
CREATE TABLE notificacion (
    id_notificacion INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT CHECK (tipo IN ('eliminacion', 'advertencia')),
    contenido TEXT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TEXT CHECK (estado IN ('activa', 'resuelta')),
    id_usuario INTEGER NOT NULL,
    id_publicacion INTEGER,
    id_sesion INTEGER,
    id_administrador INTEGER,
    FOREIGN KEY (id_administrador) REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    FOREIGN KEY (id_publicacion) REFERENCES publicacion (id_publicacion),
    FOREIGN KEY (id_sesion) REFERENCES sesion_chat (id_sesion)
);
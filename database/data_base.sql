CREATE TABLE
    rol (
        id_rol SERIAL PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL,
        permisos JSONB DEFAULT '{}'
    );

CREATE TABLE
    usuario (
        id_usuario SERIAL PRIMARY KEY,
        nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
        contraseña VARCHAR(255) NOT NULL,
        nombres VARCHAR(100) NOT NULL,
        apellidos VARCHAR(100) NOT NULL,
        edad INT CHECK (edad >= 13),
        email VARCHAR(150) UNIQUE NOT NULL,
        telefono VARCHAR(20),
        pais VARCHAR(50),
        estado VARCHAR(50),
        ciudad VARCHAR(50),
        foto_perfil TEXT,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        estado_cuenta VARCHAR(20) CHECK (
            estado_cuenta IN ('activo', 'inactivo', 'bloqueado')
        ),
        email_verificado BOOLEAN DEFAULT FALSE,
        token_verificacion VARCHAR(255),
        token_recuperacion VARCHAR(255),
        expiracion_token TIMESTAMP,
        id_rol INT NOT NULL,
        FOREIGN KEY (id_rol) REFERENCES rol (id_rol)
    );

CREATE TABLE
    interes (
        id_interes SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        categoria VARCHAR(100)
    );

CREATE TABLE
    usuario_interes (
        id_usuario INT NOT NULL,
        id_interes INT NOT NULL,
        PRIMARY KEY (id_usuario, id_interes),
        FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
        FOREIGN KEY (id_interes) REFERENCES interes (id_interes)
    );

CREATE TABLE
    publicacion (
        id_publicacion SERIAL PRIMARY KEY,
        texto TEXT NOT NULL,
        imagen TEXT,
        fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        estado VARCHAR(20) CHECK (estado IN ('visible', 'oculto', 'eliminado')),
        id_usuario INT NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
    );

CREATE TABLE
    sesion_chat (
        id_sesion SERIAL PRIMARY KEY,
        nombre_tema VARCHAR(100) NOT NULL,
        tipo VARCHAR(20) CHECK (tipo IN ('privado', 'público')),
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        estado VARCHAR(20) CHECK (estado IN ('activa', 'cerrada', 'eliminada')),
        anfitrion_id INT NOT NULL,
        FOREIGN KEY (anfitrion_id) REFERENCES usuario (id_usuario)
    );

CREATE TABLE
    usuario_sesion_chat (
        id_usuario INT NOT NULL,
        id_sesion INT NOT NULL,
        PRIMARY KEY (id_usuario, id_sesion),
        FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
        FOREIGN KEY (id_sesion) REFERENCES sesion_chat (id_sesion)
    );

CREATE TABLE
    mensaje (
        id_mensaje SERIAL PRIMARY KEY,
        contenido TEXT NOT NULL,
        imagen TEXT,
        fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        id_remitente INT NOT NULL,
        id_sesion INT NOT NULL,
        FOREIGN KEY (id_remitente) REFERENCES usuario (id_usuario),
        FOREIGN KEY (id_sesion) REFERENCES sesion_chat (id_sesion)
    );

CREATE TABLE
    solicitud_amistad (
        id_solicitud SERIAL PRIMARY KEY,
        mensaje TEXT,
        estado VARCHAR(20) CHECK (estado IN ('pendiente', 'aceptada', 'rechazada')),
        fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        remitente_id INT NOT NULL,
        destinatario_id INT NOT NULL,
        FOREIGN KEY (remitente_id) REFERENCES usuario (id_usuario),
        FOREIGN KEY (destinatario_id) REFERENCES usuario (id_usuario),
        CONSTRAINT no_auto_amistad CHECK (remitente_id <> destinatario_id)
    );

CREATE TABLE
    contacto (
        id_contacto SERIAL PRIMARY KEY,
        usuario_id_1 INT NOT NULL,
        usuario_id_2 INT NOT NULL,
        fecha_aceptacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id_1) REFERENCES usuario (id_usuario),
        FOREIGN KEY (usuario_id_2) REFERENCES usuario (id_usuario),
        CONSTRAINT no_contacto_con_sí_mismo CHECK (usuario_id_1 <> usuario_id_2)
    );

CREATE TABLE
    faq (
        id_faq SERIAL PRIMARY KEY,
        pregunta TEXT NOT NULL,
        respuesta TEXT NOT NULL
    );

CREATE TABLE
    notificacion (
        id_notificacion SERIAL PRIMARY KEY,
        tipo VARCHAR(50) CHECK (tipo IN ('eliminacion', 'advertencia')),
        contenido TEXT NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        estado VARCHAR(20) CHECK (estado IN ('activa', 'resuelta')),
        id_usuario INT NOT NULL,
        id_publicacion INT,
        id_sesion INT,
        id_administrador INT NULL,
        FOREIGN KEY (id_administrador) REFERENCES usuario (id_usuario),
        FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
        FOREIGN KEY (id_publicacion) REFERENCES publicacion (id_publicacion),
        FOREIGN KEY (id_sesion) REFERENCES sesion_chat (id_sesion)
    );
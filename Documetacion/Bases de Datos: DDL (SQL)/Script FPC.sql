DROP DATABASE IF EXISTS FULLPAINTT;
CREATE DATABASE FULLPAINTT;
USE FULLPAINTT;

-- Tabla de roles (Ya está en 3FN)
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla de tipos de identificación (Extraída para normalizar)
CREATE TABLE tipos_identificacion (
    tipo_id VARCHAR(2) PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);

-- Tabla de usuarios (Normalizada)
CREATE TABLE usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(100) UNIQUE NOT NULL,
    tipo_identificacion VARCHAR(2) NOT NULL,
    numero_identificacion VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    rol_id INT,
    foto_perfil VARCHAR(255) DEFAULT 'static/img/default-profile.png',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE SET NULL,
    FOREIGN KEY (tipo_identificacion) REFERENCES tipos_identificacion(tipo_id)
);

-- Tabla de estados de vehículo (Extraída para normalizar)
CREATE TABLE estados_vehiculo (
    estado_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Tabla de tipos de vehículo (Extraída para normalizar)
CREATE TABLE tipos_vehiculo (
    tipo_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla de marcas de vehículo (Extraída para normalizar)
CREATE TABLE marcas_vehiculo (
    marca_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla de colores (Extraída para normalizar)
CREATE TABLE colores (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Tabla de vehículos (Normalizada)
CREATE TABLE vehiculos (
    vehiculo_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    marca_id INT NOT NULL,
    modelo VARCHAR(100),
    anio INT,
    placa VARCHAR(20) UNIQUE,
    color_id INT NOT NULL,
    tipo_id INT NOT NULL,
    imagen VARCHAR(255) DEFAULT 'static/img/default-car.png',
    estado_id VARCHAR(20) DEFAULT 'sin_servicio',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (marca_id) REFERENCES marcas_vehiculo(marca_id),
    FOREIGN KEY (color_id) REFERENCES colores(color_id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_vehiculo(tipo_id),
    FOREIGN KEY (estado_id) REFERENCES estados_vehiculo(estado_id)
);

-- Tabla de categorías de servicio (Nueva tabla para normalizar)
CREATE TABLE categorias_servicio (
    categoria_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de servicios (Normalizada)
CREATE TABLE servicios (
    servicio_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    categoria_id INT NOT NULL,
    imagen VARCHAR(255),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias_servicio(categoria_id)
);

-- Tabla de estados de cotización (Extraída para normalizar)
CREATE TABLE estados_cotizacion (
    estado_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Gestión de cotizaciones (Normalizada)
CREATE TABLE cotizaciones (
    cotizacion_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    vehiculo_id INT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2),
    estado_id VARCHAR(20) DEFAULT 'pendiente',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(vehiculo_id) ON DELETE SET NULL,
    FOREIGN KEY (estado_id) REFERENCES estados_cotizacion(estado_id)
);

-- Relación: servicios incluidos en una cotización (Ya estaba en 3FN)
CREATE TABLE cotizacion_servicio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cotizacion_id INT,
    servicio_id INT,
    cantidad INT DEFAULT 1,
    subtotal DECIMAL(10,2),
    FOREIGN KEY (cotizacion_id) REFERENCES cotizaciones(cotizacion_id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicios(servicio_id)
);

-- Tabla de estados de reserva (Extraída para normalizar)
CREATE TABLE estados_reserva (
    estado_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Reservas de servicios asociadas a cotizaciones (Normalizada)
CREATE TABLE reservas (
    reserva_id INT AUTO_INCREMENT PRIMARY KEY,
    cotizacion_id INT,
    vehiculo_id INT NOT NULL,
    usuario_id INT,
    fecha DATE,
    hora TIME,
    comentario TEXT,
    total DECIMAL(10, 2),
    estado_id VARCHAR(20) DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    calificacion INT,
    comentario_calificacion TEXT,
    motivo_cancelacion VARCHAR(100),
    comentario_cancelacion TEXT,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cotizacion_id) REFERENCES cotizaciones(cotizacion_id) ON DELETE SET NULL,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(vehiculo_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (estado_id) REFERENCES estados_reserva(estado_id),
    CHECK (calificacion IS NULL OR calificacion BETWEEN 1 AND 5)
);

-- Tabla de estados de proceso (Extraída para normalizar)
CREATE TABLE estados_proceso (
    estado_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Tabla: procesos (Normalizada)
CREATE TABLE procesos (
    proceso_id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_fin DATETIME,
    empleado_id INT,
    estado_id VARCHAR(20) DEFAULT 'en_espera',
    FOREIGN KEY (reserva_id) REFERENCES reservas(reserva_id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (estado_id) REFERENCES estados_proceso(estado_id)
);

-- Tabla de tipos de reporte (Extraída para normalizar)
CREATE TABLE tipos_reporte (
    tipo_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Tabla: reportes (Normalizada)
CREATE TABLE reportes (
    reporte_id INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id INT,
    proceso_id INT,
    usuario_id INT, -- empleado que hace el reporte
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(vehiculo_id),
    FOREIGN KEY (proceso_id) REFERENCES procesos(proceso_id) ON DELETE SET NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_reporte(tipo_id)
);

-- Tabla de tipos de archivo (Extraída para normalizar)
CREATE TABLE tipos_archivo (
    tipo_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Tabla: historial de imágenes y videos del proceso (Normalizada)
CREATE TABLE archivos_proceso (
    archivo_id INT AUTO_INCREMENT PRIMARY KEY,
    proceso_id INT,
    reporte_id INT,
    tipo_id VARCHAR(20) NOT NULL,
    archivo_url VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (proceso_id) REFERENCES procesos(proceso_id) ON DELETE CASCADE,
    FOREIGN KEY (reporte_id) REFERENCES reportes(reporte_id) ON DELETE CASCADE,
    FOREIGN KEY (tipo_id) REFERENCES tipos_archivo(tipo_id)
);

-- Tabla de tipos de mensaje (Extraída para normalizar)
CREATE TABLE tipos_mensaje (
    tipo_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Tabla: mensajes de chat entre cliente y empleado (Normalizada)
CREATE TABLE chat (
    mensaje_id INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id INT,
    remitente_id INT, -- usuario que envía
    receptor_id INT,  -- usuario que recibe
    mensaje TEXT,
    tipo_id VARCHAR(20) DEFAULT 'texto',
    archivo_url VARCHAR(255),
    leido BOOLEAN DEFAULT FALSE,
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(vehiculo_id) ON DELETE CASCADE,
    FOREIGN KEY (remitente_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (receptor_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_mensaje(tipo_id)
);

-- Tabla: historial de servicios (Ya estaba en 3FN)
CREATE TABLE historial_servicios (
    historial_id INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id INT,
    reserva_id INT,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    costo_total DECIMAL(10, 2),
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(vehiculo_id),
    FOREIGN KEY (reserva_id) REFERENCES reservas(reserva_id) ON DELETE SET NULL
);

-- Tabla: bitácora para cambios (Ya estaba en 3FN)
CREATE TABLE bitacora (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    accion VARCHAR(255),
    tabla_afectada VARCHAR(50),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

-- Tabla para el carrito de compras temporal (Ya estaba en 3FN)
CREATE TABLE carrito_temporal (
    carrito_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    servicio_id INT NOT NULL,
    cantidad INT DEFAULT 1,
    fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicios(servicio_id)
);

-- Tabla para calificaciones de servicios (Ya estaba en 3FN)
CREATE TABLE calificaciones (
    calificacion_id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    usuario_id INT NOT NULL,
    puntuacion INT NOT NULL CHECK (puntuacion BETWEEN 1 AND 5),
    comentario TEXT,
    fecha_calificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reserva_id) REFERENCES reservas(reserva_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);
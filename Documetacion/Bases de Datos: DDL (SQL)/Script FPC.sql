DROP DATABASE IF EXISTS FULLPAINTT;
CREATE DATABASE FULLPAINTT;
USE FULLPAINTT;

-- Tabla de roles (Ya está en 3FN)
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO roles (nombre) VALUES ('admin'), ('empleado'), ('cliente');

-- Tabla de tipos de identificación (Extraída para normalizar)
CREATE TABLE tipos_identificacion (
    tipo_id VARCHAR(2) PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);

INSERT INTO tipos_identificacion (tipo_id, descripcion) VALUES 
('cc', 'Cédula de Ciudadanía'),
('ti', 'Tarjeta de Identidad'),
('ce', 'Cédula de Extranjería'),
('pp', 'Pasaporte'),
-- Nuevos
('nit', 'Numero de identificacion tributaria'),
('pep', 'Permiso Especial de Permanencia');

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

INSERT INTO estados_vehiculo (estado_id, descripcion) VALUES 
('sin_servicio', 'Sin servicio'),
('en_servicio', 'En servicio'),
('finalizado', 'Finalizado');

-- Tabla de tipos de vehículo (Extraída para normalizar)
CREATE TABLE tipos_vehiculo (
    tipo_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Insertar tipos comunes de vehículos
INSERT INTO tipos_vehiculo (nombre) VALUES 
('Sedan'), ('SUV'), ('Hatchback'), ('Pickup'), ('Deportivo'), ('Furgoneta'), ('Camión');

-- Tabla de marcas de vehículo (Extraída para normalizar)
CREATE TABLE marcas_vehiculo (
    marca_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

-- Insertar marcas comunes
INSERT INTO marcas_vehiculo (nombre) VALUES 
('Toyota'), ('Honda'), ('Chevrolet'), ('Ford'), ('Nissan'), ('Mazda'), ('Renault'), ('Volkswagen');

-- Tabla de colores (Extraída para normalizar)
CREATE TABLE colores (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Insertar colores comunes
INSERT INTO colores (nombre) VALUES 
('Blanco'), ('Negro'), ('Gris'), ('Plata'), ('Rojo'), ('Azul'), ('Verde'), ('Amarillo');

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

-- Insertar categorías básicas
INSERT INTO categorias_servicio (nombre, descripcion) VALUES
('Pintura', 'Servicios relacionados con la pintura del vehículo'),
('Limpieza', 'Servicios de limpieza y mantenimiento estético'),
('Restauración', 'Servicios de reparación y restauración'),
('Protección', 'Servicios de protección para la carrocería');

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

-- Actualizamos la inserción de servicios para incluir la categoría
INSERT INTO servicios (nombre, descripcion, precio, categoria_id, imagen) VALUES
('Latonería y pintura automotriz', 'Restauración completa de la carrocería y pintura de tu vehículo. Deja tu automóvil como nuevo.', 500000, 3, 'static/img/servicios/latoneria.jpg'),
('Porcelanizado', 'Tratamiento profesional que devuelve el brillo original a la pintura de tu vehículo y proporciona una capa protectora de larga duración.', 350000, 1, 'static/img/servicios/porcelanizado.png'),
('Brillada básica', 'Limpieza exterior completa que deja tu vehículo con un acabado brillante y protegido.', 40000, 2, 'static/img/servicios/brillada.jpg'),
('Desmanchado', 'Eliminación profesional de manchas difíciles en la pintura, tapicería o vidrios de tu vehículo.', 54990, 2, 'static/img/servicios/desmanchado.jpg'),
('Alistamiento interno', 'Limpieza profunda y acondicionamiento del interior de tu vehículo, dejando un ambiente fresco y renovado.', 80000, 2, 'static/img/servicios/alistamiento.jpg'),
('Lavado de motor', 'Limpieza profunda del compartimento del motor, eliminando grasa y suciedad acumulada para un mejor funcionamiento.', 80000, 2, 'static/img/servicios/lavado_motor.jpg'),
('Pulido y encerado', 'Proceso de restauración del brillo de la pintura seguido de una capa protectora de cera para mayor duración.', 150000, 1, 'static/img/servicios/pulido.jpg'),
('Restauración de faros', 'Pulido y restauración de faros opacos o amarillentos, mejorando la visibilidad y apariencia de tu vehículo.', 50000, 3, 'static/img/servicios/faros.jpg'),
('Protección de pintura con película transparente (PPF)', 'Instalación de una película protectora invisible que protege la pintura de tu vehículo contra rayones, piedras y otros elementos.', 1200000, 4, 'static/img/servicios/ppf.jpg'),
('Reparación de abolladuras sin pintura (PDR)', 'Técnica especializada para remover abolladuras sin dañar la pintura original de tu vehículo.', 200000, 3, 'static/img/servicios/pdr.jpg'),
('Polichado', 'Proceso detallado de pulido que elimina imperfecciones superficiales y restaura el brillo profundo de la pintura.', 130000, 1, 'static/img/servicios/polichado.jpeg');

-- Tabla de estados de cotización (Extraída para normalizar)
CREATE TABLE estados_cotizacion (
    estado_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

INSERT INTO estados_cotizacion (estado_id, descripcion) VALUES 
('pendiente', 'Pendiente de revisión'),
('aceptada', 'Aceptada por el cliente'),
('rechazada', 'Rechazada por el cliente');

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

INSERT INTO estados_reserva (estado_id, descripcion) VALUES 
('pendiente', 'Pendiente de inicio'),
('en_proceso', 'En proceso de servicio'),
('completada', 'Servicio completado'),
('cancelada', 'Servicio cancelado');

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

INSERT INTO estados_proceso (estado_id, descripcion) VALUES 
('en_espera', 'En espera de inicio'),
('en_proceso', 'En proceso de ejecución'),
('terminado', 'Proceso terminado');

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

INSERT INTO tipos_reporte (tipo_id, descripcion) VALUES 
('ingreso', 'Reporte de ingreso de vehículo'),
('proceso', 'Reporte durante el proceso de servicio'),
('salida', 'Reporte de salida y entrega');

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

INSERT INTO tipos_archivo (tipo_id, descripcion) VALUES 
('imagen', 'Archivo de imagen'),
('video', 'Archivo de video'),
('pdf', 'Documento PDF'),
('audio', 'Archivo de audio');

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

INSERT INTO tipos_mensaje (tipo_id, descripcion) VALUES 
('texto', 'Mensaje de texto'),
('imagen', 'Archivo de imagen'),
('audio', 'Archivo de audio'),
('archivo', 'Otro tipo de archivo');

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
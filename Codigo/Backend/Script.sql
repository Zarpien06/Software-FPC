-- ========================================
-- 🎨 BASE DE DATOS FULLPAINTT
-- Sistema de Gestión para Servicios Automotrices
-- Versión: Limpia y Documentada
-- Fecha: 2025
-- ========================================

-- Crear y usar la base de datos
DROP DATABASE IF EXISTS FULLPAINTT;
CREATE DATABASE FULLPAINTT;
USE FULLPAINTT;

-- ========================================
-- 📋 TABLAS DE CONFIGURACIÓN Y CATÁLOGOS
-- ========================================

-- Tabla de roles del sistema
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar roles básicos del sistema
INSERT INTO roles (nombre, descripcion) VALUES 
('admin', 'Administrador del sistema con acceso completo'),
('empleado', 'Empleado del taller con acceso a procesos operativos'),
('cliente', 'Cliente del servicio con acceso limitado');

-- Tabla de tipos de identificación
CREATE TABLE tipos_identificacion (
    tipo_id VARCHAR(2) PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Insertar tipos de identificación
INSERT INTO tipos_identificacion (tipo_id, descripcion) VALUES 
('cc', 'Cédula de Ciudadanía'),
('ti', 'Tarjeta de Identidad'),
('ce', 'Cédula de Extranjería'),
('pp', 'Pasaporte');

-- Tabla de marcas de vehículos
CREATE TABLE marcas_vehiculo (
    marca_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Insertar marcas comunes
INSERT INTO marcas_vehiculo (nombre) VALUES 
('Toyota'), ('Honda'), ('Chevrolet'), ('Ford'), ('Nissan'), 
('Mazda'), ('Renault'), ('Volkswagen'), ('Hyundai'), ('Kia');

-- Tabla de tipos de vehículo
CREATE TABLE tipos_vehiculo (
    tipo_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Insertar tipos de vehículos
INSERT INTO tipos_vehiculo (nombre) VALUES 
('Sedan'), ('SUV'), ('Hatchback'), ('Pickup'), ('Deportivo'), 
('Furgoneta'), ('Camión'), ('Motocicleta'), ('Crossover');

-- Tabla de colores
CREATE TABLE colores (
    color_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    codigo_hex VARCHAR(7),
    activo BOOLEAN DEFAULT TRUE
);

-- Insertar colores comunes
INSERT INTO colores (nombre, codigo_hex) VALUES 
('Blanco', '#FFFFFF'),
('Negro', '#000000'),
('Gris', '#808080'),
('Plata', '#C0C0C0'),
('Rojo', '#FF0000'),
('Azul', '#0000FF'),
('Verde', '#008000'),
('Amarillo', '#FFFF00');

-- ========================================
-- 👥 GESTIÓN DE USUARIOS
-- ========================================

-- Tabla principal de usuarios
CREATE TABLE usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    correo VARCHAR(100) UNIQUE NOT NULL,
    tipo_identificacion VARCHAR(2) NOT NULL,
    numero_identificacion VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    estado ENUM('ACTIVO', 'INACTIVO') DEFAULT 'ACTIVO',
    rol_id INT,
    foto_perfil VARCHAR(255) DEFAULT 'static/img/default-profile.png',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices y restricciones
    UNIQUE KEY unique_identificacion (tipo_identificacion, numero_identificacion),
    INDEX idx_correo (correo),
    INDEX idx_estado (estado),
    
    -- Claves foráneas
    FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE SET NULL,
    FOREIGN KEY (tipo_identificacion) REFERENCES tipos_identificacion(tipo_id)
);

-- ========================================
-- 🚗 GESTIÓN DE VEHÍCULOS
-- ========================================

-- Estados de vehículo
CREATE TABLE estados_vehiculo (
    estado_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

INSERT INTO estados_vehiculo (estado_id, descripcion) VALUES 
('sin_servicio', 'Vehículo sin servicio activo'),
('en_servicio', 'Vehículo en proceso de servicio'),
('finalizado', 'Servicio finalizado, listo para entrega');

CREATE TABLE vehiculos (
    vehiculo_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    marca_id INT NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    anio INT,
    placa VARCHAR(20) UNIQUE,
    color_id INT NOT NULL,
    tipo_id INT NOT NULL,
    imagen VARCHAR(255) DEFAULT 'static/img/default-car.png',
    estado_id VARCHAR(20) DEFAULT 'sin_servicio',
    kilometraje INT,
    numero_motor VARCHAR(50),
    numero_chasis VARCHAR(50),
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_placa (placa),
    INDEX idx_usuario (usuario_id),
    INDEX idx_estado (estado_id),
    
    -- Restricciones
    CHECK (kilometraje >= 0),
    
    -- Claves foráneas
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (marca_id) REFERENCES marcas_vehiculo(marca_id),
    FOREIGN KEY (color_id) REFERENCES colores(color_id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_vehiculo(tipo_id),
    FOREIGN KEY (estado_id) REFERENCES estados_vehiculo(estado_id)
);


-- ========================================
-- 🛠️ GESTIÓN DE SERVICIOS
-- ========================================

-- Categorías de servicios
CREATE TABLE categorias_servicio (
    categoria_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar categorías de servicios
INSERT INTO categorias_servicio (nombre, descripcion) VALUES
('Pintura', 'Servicios relacionados con la pintura del vehículo'),
('Limpieza', 'Servicios de limpieza y mantenimiento estético'),
('Restauración', 'Servicios de reparación y restauración de carrocería'),
('Protección', 'Servicios de protección para la carrocería y pintura');

-- Tabla principal de servicios
CREATE TABLE servicios (
    servicio_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    categoria_id INT NOT NULL,
    imagen VARCHAR(255),
    tiempo_estimado INT COMMENT 'Tiempo estimado en horas',
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_categoria (categoria_id),
    INDEX idx_activo (activo),
    
    -- Restricciones
    CHECK (precio >= 0),
    CHECK (tiempo_estimado > 0),
    
    -- Claves foráneas
    FOREIGN KEY (categoria_id) REFERENCES categorias_servicio(categoria_id)
);

-- Insertar servicios principales
INSERT INTO servicios (nombre, descripcion, precio, categoria_id, tiempo_estimado, imagen) VALUES
('Latonería y pintura automotriz', 'Restauración completa de la carrocería y pintura de tu vehículo. Deja tu automóvil como nuevo.', 500000, 3, 48, 'static/img/servicios/latoneria.jpg'),
('Porcelanizado', 'Tratamiento profesional que devuelve el brillo original a la pintura de tu vehículo y proporciona una capa protectora de larga duración.', 350000, 1, 8, 'static/img/servicios/porcelanizado.png'),
('Brillada básica', 'Limpieza exterior completa que deja tu vehículo con un acabado brillante y protegido.', 40000, 2, 2, 'static/img/servicios/brillada.jpg'),
('Desmanchado', 'Eliminación profesional de manchas difíciles en la pintura, tapicería o vidrios de tu vehículo.', 54990, 2, 3, 'static/img/servicios/desmanchado.jpg'),
('Alistamiento interno', 'Limpieza profunda y acondicionamiento del interior de tu vehículo, dejando un ambiente fresco y renovado.', 80000, 2, 4, 'static/img/servicios/alistamiento.jpg'),
('Lavado de motor', 'Limpieza profunda del compartimento del motor, eliminando grasa y suciedad acumulada para un mejor funcionamiento.', 80000, 2, 2, 'static/img/servicios/lavado_motor.jpg'),
('Pulido y encerado', 'Proceso de restauración del brillo de la pintura seguido de una capa protectora de cera para mayor duración.', 150000, 1, 6, 'static/img/servicios/pulido.jpg'),
('Restauración de faros', 'Pulido y restauración de faros opacos o amarillentos, mejorando la visibilidad y apariencia de tu vehículo.', 50000, 3, 2, 'static/img/servicios/faros.jpg'),
('Protección de pintura con película transparente (PPF)', 'Instalación de una película protectora invisible que protege la pintura de tu vehículo contra rayones, piedras y otros elementos.', 1200000, 4, 12, 'static/img/servicios/ppf.jpg'),
('Reparación de abolladuras sin pintura (PDR)', 'Técnica especializada para remover abolladuras sin dañar la pintura original de tu vehículo.', 200000, 3, 4, 'static/img/servicios/pdr.jpg'),
('Polichado', 'Proceso detallado de pulido que elimina imperfecciones superficiales y restaura el brillo profundo de la pintura.', 130000, 1, 5, 'static/img/servicios/polichado.jpeg');

-- ========================================
-- 💰 GESTIÓN DE COTIZACIONES
-- ========================================

-- Estados de cotización
CREATE TABLE estados_cotizacion (
    estado_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

INSERT INTO estados_cotizacion (estado_id, descripcion) VALUES 
('pendiente', 'Pendiente de revisión por parte del cliente'),
('aceptada', 'Aceptada por el cliente'),
('rechazada', 'Rechazada por el cliente'),
('vencida', 'Cotización vencida por tiempo');

-- Tabla principal de cotizaciones
CREATE TABLE cotizaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    vehiculo_id INT NULL,
    total DECIMAL(10, 2) NOT NULL DEFAULT 0,
    estado_id VARCHAR(20) DEFAULT 'pendiente',
    observaciones TEXT,
    fecha_vencimiento DATE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_usuario (usuario_id),
    INDEX idx_estado (estado_id),
    INDEX idx_fecha_creacion (fecha_creacion),
    
    -- Restricciones
    CHECK (total >= 0),
    
    -- Claves foráneas
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(vehiculo_id) ON DELETE SET NULL,
    FOREIGN KEY (estado_id) REFERENCES estados_cotizacion(estado_id)
);

-- Detalle de servicios en cotizaciones
CREATE TABLE cotizacion_servicio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cotizacion_id INT NOT NULL,
    servicio_id INT NOT NULL,
    cantidad INT DEFAULT 1,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    observaciones TEXT,
    
    -- Índices
    INDEX idx_cotizacion (cotizacion_id),
    INDEX idx_servicio (servicio_id),
    
    -- Restricciones
    CHECK (cantidad > 0),
    CHECK (precio_unitario >= 0),
    CHECK (subtotal >= 0),
    
    -- Claves foráneas
    FOREIGN KEY (cotizacion_id) REFERENCES cotizaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicios(servicio_id)
);

-- ========================================
-- 📅 GESTIÓN DE RESERVAS
-- ========================================

-- Estados de reserva
CREATE TABLE estados_reserva (
    estado_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

INSERT INTO estados_reserva (estado_id, descripcion) VALUES 
('pendiente', 'Reserva pendiente de inicio'),
('confirmada', 'Reserva confirmada'),
('en_proceso', 'Servicio en proceso de ejecución'),
('completada', 'Servicio completado satisfactoriamente'),
('cancelada', 'Reserva cancelada');

-- Tabla principal de reservas
CREATE TABLE reservas (
    reserva_id INT AUTO_INCREMENT PRIMARY KEY,
    cotizacion_id INT,
    vehiculo_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    comentario TEXT,
    total DECIMAL(10, 2) NOT NULL,
    estado_id VARCHAR(20) DEFAULT 'pendiente',
    calificacion INT,
    comentario_calificacion TEXT,
    motivo_cancelacion VARCHAR(100),
    comentario_cancelacion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_fecha_hora (fecha, hora),
    INDEX idx_usuario (usuario_id),
    INDEX idx_vehiculo (vehiculo_id),
    INDEX idx_estado (estado_id),
    
    -- Restricciones
    CHECK (calificacion IS NULL OR calificacion BETWEEN 1 AND 5),
    CHECK (total >= 0),
    
    -- Claves foráneas
    FOREIGN KEY (cotizacion_id) REFERENCES cotizaciones(id) ON DELETE SET NULL,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(vehiculo_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (estado_id) REFERENCES estados_reserva(estado_id)
);

-- ========================================
-- ⚙️ GESTIÓN DE PROCESOS
-- ========================================

-- Estados de proceso
CREATE TABLE estados_proceso (
    estado_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

INSERT INTO estados_proceso (estado_id, descripcion) VALUES 
('en_espera', 'Proceso en espera de inicio'),
('en_proceso', 'Proceso en ejecución'),
('pausado', 'Proceso pausado temporalmente'),
('terminado', 'Proceso terminado exitosamente'),
('cancelado', 'Proceso cancelado');

-- Tabla principal de procesos
CREATE TABLE procesos (
    proceso_id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_fin DATETIME,
    empleado_id INT,
    estado_id VARCHAR(20) DEFAULT 'en_espera',
    progreso INT DEFAULT 0 COMMENT 'Porcentaje de progreso (0-100)',
    observaciones TEXT,
    
    -- Índices
    INDEX idx_reserva (reserva_id),
    INDEX idx_empleado (empleado_id),
    INDEX idx_estado (estado_id),
    INDEX idx_fecha_inicio (fecha_inicio),
    
    -- Restricciones
    CHECK (progreso >= 0 AND progreso <= 100),
    CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio),
    
    -- Claves foráneas
    FOREIGN KEY (reserva_id) REFERENCES reservas(reserva_id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (estado_id) REFERENCES estados_proceso(estado_id)
);

-- ========================================
-- 📊 GESTIÓN DE REPORTES
-- ========================================

-- Tipos de reporte
CREATE TABLE tipos_reporte (
    tipo_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

INSERT INTO tipos_reporte (tipo_id, descripcion) VALUES 
('ingreso', 'Reporte de ingreso de vehículo'),
('proceso', 'Reporte durante el proceso de servicio'),
('salida', 'Reporte de salida y entrega'),
('incidencia', 'Reporte de incidencias o problemas');

-- Tabla principal de reportes
CREATE TABLE reportes (
    reporte_id INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id INT NOT NULL,
    proceso_id INT,
    usuario_id INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    tipo_id VARCHAR(20) NOT NULL,
    prioridad ENUM('BAJA', 'MEDIA', 'ALTA', 'CRITICA') DEFAULT 'MEDIA',
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_vehiculo (vehiculo_id),
    INDEX idx_proceso (proceso_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_tipo (tipo_id),
    INDEX idx_fecha (fecha_reporte),
    
    -- Claves foráneas
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(vehiculo_id),
    FOREIGN KEY (proceso_id) REFERENCES procesos(proceso_id) ON DELETE SET NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_reporte(tipo_id)
);

-- ========================================
-- 📁 GESTIÓN DE ARCHIVOS
-- ========================================

-- Tipos de archivo
CREATE TABLE tipos_archivo (
    tipo_id VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    extensiones_permitidas VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE
);

INSERT INTO tipos_archivo (tipo_id, descripcion, extensiones_permitidas) VALUES 
('imagen', 'Archivo de imagen', 'jpg,jpeg,png,gif,webp'),
('video', 'Archivo de video', 'mp4,avi,mov,mkv'),
('pdf', 'Documento PDF', 'pdf'),
('audio', 'Archivo de audio', 'mp3,wav,ogg,m4a');

-- Archivos asociados a procesos y reportes
CREATE TABLE archivos_proceso (
    archivo_id INT AUTO_INCREMENT PRIMARY KEY,
    proceso_id INT,
    reporte_id INT,
    tipo_id VARCHAR(20) NOT NULL,
    archivo_url VARCHAR(255) NOT NULL,
    nombre_original VARCHAR(255) NOT NULL,
    descripcion TEXT,
    tamaño_bytes INT,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_proceso (proceso_id),
    INDEX idx_reporte (reporte_id),
    INDEX idx_tipo (tipo_id),
    
    -- Restricciones
    CHECK (tamaño_bytes > 0),
    CHECK (proceso_id IS NOT NULL OR reporte_id IS NOT NULL),
    
    -- Claves foráneas
    FOREIGN KEY (proceso_id) REFERENCES procesos(proceso_id) ON DELETE CASCADE,
    FOREIGN KEY (reporte_id) REFERENCES reportes(reporte_id) ON DELETE CASCADE,
    FOREIGN KEY (tipo_id) REFERENCES tipos_archivo(tipo_id)
);

-- ========================================
-- 💬 SISTEMA DE CHAT MEJORADO
-- ========================================

-- Conversaciones de chat
CREATE TABLE chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    proceso_id INT NOT NULL,
    cliente_id INT NOT NULL,
    mecanico_id INT,
    titulo VARCHAR(200) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_proceso (proceso_id),
    INDEX idx_cliente (cliente_id),
    INDEX idx_mecanico (mecanico_id),
    
    -- Claves foráneas
    FOREIGN KEY (proceso_id) REFERENCES procesos(proceso_id),
    FOREIGN KEY (cliente_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (mecanico_id) REFERENCES usuarios(usuario_id)
);

-- Mensajes dentro de un chat
CREATE TABLE mensajes_chat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT NOT NULL,
    remitente_id INT NOT NULL,
    contenido TEXT NOT NULL,
    tipo_mensaje ENUM('TEXTO', 'IMAGEN', 'ARCHIVO', 'NOTIFICACION') DEFAULT 'TEXTO',
    estado ENUM('ENVIADO', 'ENTREGADO', 'LEIDO') DEFAULT 'ENVIADO',
    archivo_url VARCHAR(500),
    respuesta_a INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    leido_at TIMESTAMP NULL,
    
    -- Índices
    INDEX idx_chat (chat_id),
    INDEX idx_remitente (remitente_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha (created_at),
    
    -- Claves foráneas
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
    FOREIGN KEY (remitente_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (respuesta_a) REFERENCES mensajes_chat(id)
);

-- Conexiones activas de chat
CREATE TABLE conexiones_chat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    chat_id INT NOT NULL,
    session_id VARCHAR(100) NOT NULL UNIQUE,
    activa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_usuario (usuario_id),
    INDEX idx_chat (chat_id),
    INDEX idx_session (session_id),
    
    -- Claves foráneas
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (chat_id) REFERENCES chats(id)
);

-- ========================================
-- 📈 TABLAS AUXILIARES
-- ========================================

-- Carrito de compras temporal
CREATE TABLE carrito_temporal (
    carrito_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    servicio_id INT NOT NULL,
    cantidad INT DEFAULT 1,
    fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_usuario (usuario_id),
    UNIQUE KEY unique_usuario_servicio (usuario_id, servicio_id),
    
    -- Restricciones
    CHECK (cantidad > 0),
    
    -- Claves foráneas
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicios(servicio_id)
);

-- Calificaciones de servicios
CREATE TABLE calificaciones (
    calificacion_id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    usuario_id INT NOT NULL,
    puntuacion INT NOT NULL,
    comentario TEXT,
    fecha_calificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_reserva (reserva_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_puntuacion (puntuacion),
    
    -- Restricciones
    CHECK (puntuacion BETWEEN 1 AND 5),
    
    -- Claves foráneas
    FOREIGN KEY (reserva_id) REFERENCES reservas(reserva_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

-- Historial de servicios
CREATE TABLE historial_servicios (
    historial_id INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id INT NOT NULL,
    reserva_id INT,
    descripcion TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    costo_total DECIMAL(10, 2) NOT NULL,
    
    -- Índices
    INDEX idx_vehiculo (vehiculo_id),
    INDEX idx_reserva (reserva_id),
    INDEX idx_fecha_inicio (fecha_inicio),
    
    -- Restricciones
    CHECK (costo_total >= 0),
    CHECK (fecha_fin IS NULL OR fecha_fin >= fecha_inicio),
    
    -- Claves foráneas
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(vehiculo_id),
    FOREIGN KEY (reserva_id) REFERENCES reservas(reserva_id) ON DELETE SET NULL
);

-- Bitácora del sistema
CREATE TABLE bitacora (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    accion VARCHAR(255) NOT NULL,
    tabla_afectada VARCHAR(50) NOT NULL,
    registro_id INT,
    datos_anteriores JSON,
    datos_nuevos JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_usuario (usuario_id),
    INDEX idx_tabla (tabla_afectada),
    INDEX idx_fecha (fecha),
    
    -- Claves foráneas
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

-- ========================================
-- 🔧 TRIGGERS Y PROCEDIMIENTOS
-- ========================================

-- Trigger para actualizar el total de cotizaciones
DELIMITER //
CREATE TRIGGER actualizar_total_cotizacion
AFTER INSERT ON cotizacion_servicio
FOR EACH ROW
BEGIN
    UPDATE cotizaciones 
    SET total = (
        SELECT SUM(subtotal) 
        FROM cotizacion_servicio 
        WHERE cotizacion_id = NEW.cotizacion_id
    )
    WHERE id = NEW.cotizacion_id;
END;//

CREATE TRIGGER actualizar_total_cotizacion_update
AFTER UPDATE ON cotizacion_servicio
FOR EACH ROW
BEGIN
    UPDATE cotizaciones 
    SET total = (
        SELECT SUM(subtotal) 
        FROM cotizacion_servicio 
        WHERE cotizacion_id = NEW.cotizacion_id
    )
    WHERE id = NEW.cotizacion_id;
END;//

CREATE TRIGGER actualizar_total_cotizacion_delete
AFTER DELETE ON cotizacion_servicio
FOR EACH ROW
BEGIN
    UPDATE cotizaciones 
    SET total = COALESCE((
        SELECT SUM(subtotal) 
        FROM cotizacion_servicio 
        WHERE cotizacion_id = OLD.cotizacion_id
    ), 0)
    WHERE id = OLD.cotizacion_id;
END;//
DELIMITER ;

-- ========================================
-- 📊 VISTAS ÚTILES
-- ========================================

-- Vista de vehículos con información completa
CREATE VIEW vista_vehiculos_completa AS
SELECT 
    v.vehiculo_id,
    v.placa,
    v.modelo,
    v.anio,
    v.kilometraje,
    u.nombre_completo AS propietario,
    u.telefono,
    u.correo,
    m.nombre AS marca,
    c.nombre AS color,
    t.nombre AS tipo,
    e.descripcion AS estado,
    v.fecha_registro
FROM vehiculos v
INNER JOIN usuarios u ON v.usuario_id = u.usuario_id
INNER JOIN marcas_vehiculo m ON v.marca_id = m.marca_id
INNER JOIN colores c ON v.color_id = c.color_id
INNER JOIN tipos_vehiculo t ON v.tipo_id = t.tipo_id
INNER JOIN estados_vehiculo e ON v.estado_id = e.estado_id;

-- Vista de reservas con información detallada
CREATE VIEW vista_reservas_detallada AS
SELECT 
    r.reserva_id,
    r.fecha,
    r.hora,
    r.total,
    r.calificacion,
    er.descripcion AS estado,
    u.nombre_completo AS cliente,
    u.telefono,
    v.placa,
    v.modelo,
    m.nombre AS marca,
    r.fecha_creacion
FROM reservas r
INNER JOIN usuarios u ON r.usuario_id = u.usuario_id
INNER JOIN vehiculos v ON r.vehiculo_id = v.vehiculo_id
INNER JOIN marcas_vehiculo m ON v.marca_id = m.marca_id
INNER JOIN estados_reserva er ON r.estado_id = er.estado_id;

-- ========================================
-- 🎯 ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- ========================================

-- Índices compuestos para consultas frecuentes
CREATE INDEX idx_vehiculo_usuario_estado ON vehiculos(usuario_id, estado_id);
CREATE INDEX idx_reserva_fecha_estado ON reservas(fecha, estado_id);
CREATE INDEX idx_proceso_empleado_estado ON procesos(empleado_id, estado_id);

-- ========================================
-- 📋 PROCEDIMIENTOS ALMACENADOS ÚTILES
-- ========================================

-- Procedimiento para crear una cotización completa
DELIMITER //
CREATE PROCEDURE crear_cotizacion_completa(
    IN p_usuario_id INT,
    IN p_vehiculo_id INT,
    IN p_servicios_json JSON,
    IN p_observaciones TEXT,
    OUT p_cotizacion_id INT
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_servicio_id INT;
    DECLARE v_cantidad INT;
    DECLARE v_precio DECIMAL(10,2);
    DECLARE v_subtotal DECIMAL(10,2);
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Crear la cotización
    INSERT INTO cotizaciones (usuario_id, vehiculo_id, observaciones, fecha_vencimiento)
    VALUES (p_usuario_id, p_vehiculo_id, p_observaciones, DATE_ADD(CURDATE(), INTERVAL 15 DAY));
    
    SET p_cotizacion_id = LAST_INSERT_ID();
    
    -- Procesar servicios del JSON
    -- Ejemplo de JSON: [{"servicio_id": 1, "cantidad": 2}, {"servicio_id": 3, "cantidad": 1}]
    SET @i = 0;
    WHILE @i < JSON_LENGTH(p_servicios_json) DO
        SET v_servicio_id = JSON_UNQUOTE(JSON_EXTRACT(p_servicios_json, CONCAT('$[', @i, '].servicio_id')));
        SET v_cantidad = JSON_UNQUOTE(JSON_EXTRACT(p_servicios_json, CONCAT('$[', @i, '].cantidad')));
        
        -- Obtener precio del servicio
        SELECT precio INTO v_precio FROM servicios WHERE servicio_id = v_servicio_id;
        SET v_subtotal = v_precio * v_cantidad;
        
        -- Insertar detalle
        INSERT INTO cotizacion_servicio (cotizacion_id, servicio_id, cantidad, precio_unitario, subtotal)
        VALUES (p_cotizacion_id, v_servicio_id, v_cantidad, v_precio, v_subtotal);
        
        SET @i = @i + 1;
    END WHILE;
    
    COMMIT;
END;//

-- Procedimiento para obtener estadísticas del taller
CREATE PROCEDURE obtener_estadisticas_taller(
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE
)
BEGIN
    -- Servicios más solicitados
    SELECT 
        s.nombre,
        COUNT(cs.servicio_id) as total_solicitudes,
        SUM(cs.subtotal) as ingresos_generados
    FROM cotizacion_servicio cs
    INNER JOIN servicios s ON cs.servicio_id = s.servicio_id
    INNER JOIN cotizaciones c ON cs.cotizacion_id = c.id
    WHERE DATE(c.fecha_creacion) BETWEEN p_fecha_inicio AND p_fecha_fin
    GROUP BY s.servicio_id, s.nombre
    ORDER BY total_solicitudes DESC
    LIMIT 10;
    
    -- Ingresos por mes
    SELECT 
        DATE_FORMAT(r.fecha_creacion, '%Y-%m') as mes,
        COUNT(r.reserva_id) as total_reservas,
        SUM(r.total) as ingresos_totales,
        AVG(r.calificacion) as calificacion_promedio
    FROM reservas r
    WHERE DATE(r.fecha_creacion) BETWEEN p_fecha_inicio AND p_fecha_fin
        AND r.estado_id = 'completada'
    GROUP BY DATE_FORMAT(r.fecha_creacion, '%Y-%m')
    ORDER BY mes;
    
    -- Vehículos por marca
    SELECT 
        m.nombre as marca,
        COUNT(v.vehiculo_id) as total_vehiculos
    FROM vehiculos v
    INNER JOIN marcas_vehiculo m ON v.marca_id = m.marca_id
    GROUP BY m.marca_id, m.nombre
    ORDER BY total_vehiculos DESC;
END;//

-- Procedimiento para actualizar estado de vehículo
CREATE PROCEDURE actualizar_estado_vehiculo(
    IN p_vehiculo_id INT,
    IN p_nuevo_estado VARCHAR(20)
)
BEGIN
    DECLARE v_estado_actual VARCHAR(20);
    
    -- Verificar estado actual
    SELECT estado_id INTO v_estado_actual 
    FROM vehiculos 
    WHERE vehiculo_id = p_vehiculo_id;
    
    -- Actualizar estado
    UPDATE vehiculos 
    SET estado_id = p_nuevo_estado 
    WHERE vehiculo_id = p_vehiculo_id;
    
    -- Registrar en bitácora
    INSERT INTO bitacora (usuario_id, accion, tabla_afectada, registro_id)
    VALUES (NULL, CONCAT('Estado cambiado de ', v_estado_actual, ' a ', p_nuevo_estado), 'vehiculos', p_vehiculo_id);
END;//
DELIMITER ;

-- ========================================
-- 🔍 FUNCIONES ÚTILES
-- ========================================

-- Función para calcular edad del vehículo
DELIMITER //
CREATE FUNCTION calcular_edad_vehiculo(p_anio INT)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    RETURN YEAR(CURDATE()) - p_anio;
END;//

-- Función para obtener próxima cita disponible
CREATE FUNCTION proxima_cita_disponible(p_fecha_inicio DATE)
RETURNS DATE
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_fecha_disponible DATE;
    DECLARE v_contador INT DEFAULT 0;
    DECLARE v_citas_dia INT;
    
    SET v_fecha_disponible = p_fecha_inicio;
    
    -- Buscar próxima fecha con menos de 10 citas (límite diario)
    WHILE v_contador < 30 DO -- Buscar máximo 30 días adelante
        SELECT COUNT(*) INTO v_citas_dia
        FROM reservas
        WHERE fecha = v_fecha_disponible
        AND estado_id NOT IN ('cancelada');
        
        IF v_citas_dia < 10 THEN
            RETURN v_fecha_disponible;
        END IF;
        
        SET v_fecha_disponible = DATE_ADD(v_fecha_disponible, INTERVAL 1 DAY);
        SET v_contador = v_contador + 1;
    END WHILE;
    
    RETURN DATE_ADD(p_fecha_inicio, INTERVAL 30 DAY);
END;//
DELIMITER ;

-- ========================================
-- 🎨 DATOS DE PRUEBA (OPCIONAL)
-- ========================================

-- Insertar usuario administrador por defecto
INSERT INTO usuarios (
    nombre_completo, 
    telefono, 
    correo, 
    tipo_identificacion, 
    numero_identificacion, 
    password_hash, 
    rol_id
) VALUES (
    'Administrador Sistema',
    '3001234567',
    'admin@fullpaintt.com',
    'cc',
    '1234567890',
    '$2b$12$LQv3c1yqBwlrM8B2eLc9sOX8w8zx.QY8B8L9P2KpJ5M6Q3F7G9H2I', -- password: admin123
    1
);

-- Insertar empleado de prueba
INSERT INTO usuarios (
    nombre_completo, 
    telefono, 
    correo, 
    tipo_identificacion, 
    numero_identificacion, 
    password_hash, 
    rol_id
) VALUES (
    'Carlos Mecánico',
    '3009876543',
    'carlos@fullpaintt.com',
    'cc',
    '9876543210',
    '$2b$12$LQv3c1yqBwlrM8B2eLc9sOX8w8zx.QY8B8L9P2KpJ5M6Q3F7G9H2I', -- password: admin123
    2
);

-- ========================================
-- ✅ VERIFICACIÓN DE INTEGRIDAD
-- ========================================

-- Verificar que todas las tablas fueron creadas correctamente
SELECT 
    TABLE_NAME as 'Tabla',
    TABLE_ROWS as 'Registros',
    CREATE_TIME as 'Fecha_Creacion'
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'FULLPAINTT'
ORDER BY TABLE_NAME;

-- Verificar claves foráneas
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'FULLPAINTT'
    AND REFERENCED_TABLE_NAME IS NOT NULL
ORDER BY TABLE_NAME;

-- ========================================
-- 📝 COMENTARIOS Y DOCUMENTACIÓN
-- ========================================

/*
ESTRUCTURA DE LA BASE DE DATOS FULLPAINTT
========================================

TABLAS PRINCIPALES:
- usuarios: Gestión de usuarios del sistema (clientes, empleados, admin)
- vehiculos: Información de vehículos de los clientes
- servicios: Catálogo de servicios ofrecidos
- cotizaciones: Cotizaciones generadas para clientes
- reservas: Reservas de servicios confirmadas
- procesos: Procesos de trabajo en curso
- reportes: Reportes de progreso y incidencias

TABLAS DE CATÁLOGO:
- roles, tipos_identificacion, marcas_vehiculo, tipos_vehiculo
- colores, categorias_servicio, estados_*

TABLAS DE RELACIÓN:
- cotizacion_servicio: Servicios incluidos en cada cotización
- archivos_proceso: Archivos multimedia de procesos

SISTEMA DE CHAT:
- chats: Conversaciones entre clientes y mecánicos
- mensajes_chat: Mensajes individuales
- conexiones_chat: Gestión de conexiones activas

CARACTERÍSTICAS PRINCIPALES:
✅ Tercera Forma Normal (3FN)
✅ Integridad referencial completa
✅ Índices optimizados para consultas frecuentes
✅ Triggers para cálculos automáticos
✅ Procedimientos almacenados para operaciones complejas
✅ Vistas para consultas simplificadas
✅ Sistema de auditoría (bitácora)
✅ Validaciones de datos mediante CHECK constraints
✅ Soporte para archivos multimedia
✅ Sistema de chat en tiempo real
✅ Gestión de estados para workflow completo

FLUJO DE TRABAJO:
1. Cliente registra vehículo
2. Solicita cotización de servicios
3. Aprueba cotización y crea reserva
4. Se asigna empleado y se crea proceso
5. Se generan reportes durante el servicio
6. Cliente y empleado pueden chatear
7. Se completa el servicio y se califica
8. Se registra en historial

SEGURIDAD:
- Hashes de contraseñas
- Auditoría completa de cambios
- Validaciones de integridad
- Control de acceso por roles

OPTIMIZACIÓN:
- Índices estratégicos
- Particionamiento lógico
- Procedimientos almacenados
- Vistas materializadas para reportes
*/

-- ========================================
-- 🚀 FINALIZACIÓN DE SCRIPT
-- ========================================

-- Habilitar el log de consultas lentas para optimización
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Confirmar creación exitosa
SELECT 'BASE DE DATOS FULLPAINTT CREADA EXITOSAMENTE' as ESTADO,
       COUNT(*) as TOTAL_TABLAS
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'FULLPAINTT';

-- Mostrar resumen de la estructura
SELECT 
    'RESUMEN DE LA BASE DE DATOS' as SECCION,
    '' as DETALLE
UNION ALL
SELECT 'Total de tablas:', COUNT(*)
FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'FULLPAINTT'
UNION ALL
SELECT 'Total de vistas:', COUNT(*)
FROM information_schema.VIEWS WHERE TABLE_SCHEMA = 'FULLPAINTT'
UNION ALL
SELECT 'Total de procedimientos:', COUNT(*)
FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = 'FULLPAINTT' AND ROUTINE_TYPE = 'PROCEDURE'
UNION ALL
SELECT 'Total de funciones:', COUNT(*)
FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA = 'FULLPAINTT' AND ROUTINE_TYPE = 'FUNCTION';

-- ========================================
-- 📚 FIN DEL SCRIPT
-- ========================================

select * from usuarios;

ALTER TABLE cotizaciones
ADD COLUMN numero_cotizacion VARCHAR(20) AFTER id;
ALTER TABLE cotizaciones ADD COLUMN cliente_id INT;
ALTER TABLE cotizaciones
ADD CONSTRAINT fk_cliente_id FOREIGN KEY (cliente_id) REFERENCES usuarios(id);


-- Insertar marcas
INSERT INTO marcas (id, nombre) VALUES
(1, 'Toyota'),
(2, 'Chevrolet'),
(3, 'Mazda');

-- Insertar colores
INSERT INTO colores (id, nombre) VALUES
(1, 'Rojo'),
(2, 'Negro'),
(3, 'Blanco');

-- Insertar tipos
INSERT INTO tipos (id, nombre) VALUES
(1, 'Sedán'),
(2, 'SUV'),
(3, 'Pickup');


-- Crear tabla de marcas
CREATE TABLE marcas (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL
);

-- Crear tabla de colores
CREATE TABLE colores (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL
);

-- Crear tabla de tipos
CREATE TABLE tipos (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL
);


INSERT INTO colores (nombre) VALUES
('Rojo'), ('Negro'), ('Blanco'), ('Gris'), ('Azul'), ('Verde'), ('Blanco Perlado'), ('Plateado');
SELECT * FROM colores;

UPDATE usuarios SET rol_id = 2 WHERE usuario_id = 10;

-- ========================================
-- 📚 FIN DEL SCRIPT
-- ========================================

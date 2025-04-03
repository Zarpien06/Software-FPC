CREATE DATABASE IF NOT EXISTS FPC;

USE FPC;


CREATE TABLE Roles (
    rol_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) UNIQUE
);



CREATE TABLE Usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    contraseña VARCHAR(255),
    rol_id INT,
    fecha_registro DATE,
    FOREIGN KEY (rol_id) REFERENCES Roles(rol_id)
);


CREATE TABLE Clientes (
    cliente_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    direccion VARCHAR(255),
    telefono VARCHAR(15),
    fecha_registro DATE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);


CREATE TABLE Empleados (
    empleado_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    puesto VARCHAR(50),
    telefono VARCHAR(15),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

CREATE TABLE Administradores (
    administrador_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    fecha_registro DATE,
    nivel_acceso ENUM('Bajo', 'Medio', 'Alto') DEFAULT 'Alto',
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);


CREATE TABLE Vehiculos (
    vehiculo_id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    año INT,
    placa VARCHAR(10),
    tipo_vehiculo ENUM('Carro', 'Moto'),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id)
);


CREATE TABLE Servicios (
    servicio_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    descripcion TEXT,
    precio DECIMAL(10, 2)
);


CREATE TABLE Historial_Servicios (
    historial_id INT PRIMARY KEY AUTO_INCREMENT,
    vehiculo_id INT,
    servicio_id INT,
    fecha DATE,
    costo DECIMAL(10, 2),
    descripcion TEXT,
    FOREIGN KEY (vehiculo_id) REFERENCES Vehiculos(vehiculo_id),
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id)
);


CREATE TABLE Asignacion_Empleados_Servicios (
    asignacion_id INT PRIMARY KEY AUTO_INCREMENT,
    historial_id INT,
    empleado_id INT,
    FOREIGN KEY (historial_id) REFERENCES Historial_Servicios(historial_id),
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
);


CREATE TABLE Facturas (
    factura_id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT,
    fecha DATE,
    total DECIMAL(10, 2),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id)
);


CREATE TABLE Detalle_Factura (
    detalle_id INT PRIMARY KEY AUTO_INCREMENT,
    factura_id INT,
    servicio_id INT,
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    total DECIMAL(10, 2),
    FOREIGN KEY (factura_id) REFERENCES Facturas(factura_id),
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id)
);


CREATE TABLE Tipos_Proceso (
    tipo_proceso_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    descripcion TEXT
);


INSERT INTO Tipos_Proceso (nombre, descripcion) 
VALUES ('Mantenimiento Preventivo', 'Revisión y cambio de fluidos, filtros, etc.'),
       ('Reparación', 'Arreglo de fallos mecánicos y electrónicos'),
       ('Revisión General', 'Inspección completa del vehículo para detectar problemas');


CREATE TABLE Procesos (
    proceso_id INT PRIMARY KEY AUTO_INCREMENT,
    vehiculo_id INT,
    tipo_proceso_id INT,
    empleado_id INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    estado ENUM('Pendiente', 'En Proceso', 'Finalizado'),
    descripcion TEXT,
    FOREIGN KEY (vehiculo_id) REFERENCES Vehiculos(vehiculo_id),
    FOREIGN KEY (tipo_proceso_id) REFERENCES Tipos_Proceso(tipo_proceso_id),
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
);


CREATE TABLE Registro_Mantenimiento (
    mantenimiento_id INT PRIMARY KEY AUTO_INCREMENT,
    vehiculo_id INT,
    tipo_mantenimiento VARCHAR(100),
    fecha DATE,
    empleado_id INT,
    costo DECIMAL(10, 2),
    descripcion TEXT,
    FOREIGN KEY (vehiculo_id) REFERENCES Vehiculos(vehiculo_id),
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
);


CREATE TABLE Historial_Cliente (
    historial_cliente_id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT,
    fecha DATE,
    tipo_evento ENUM('Cambio de Datos', 'Queja', 'Nueva Compra', 'Observación', 'Otro'),
    descripcion TEXT,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id)
);


CREATE TABLE Historial_Servicios_Realizados (
    historial_servicio_realizado_id INT PRIMARY KEY AUTO_INCREMENT,
    vehiculo_id INT,
    servicio_id INT,
    fecha DATE,
    empleado_id INT,
    costo DECIMAL(10, 2),
    descripcion TEXT,
    FOREIGN KEY (vehiculo_id) REFERENCES Vehiculos(vehiculo_id),
    FOREIGN KEY (servicio_id) REFERENCES Servicios(servicio_id),
    FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
);


CREATE TABLE Asignacion_Proceso_Vehiculo (
    asignacion_proceso_id INT PRIMARY KEY AUTO_INCREMENT,
    vehiculo_id INT,
    proceso_id INT,
    fecha_asignacion DATE,
    estado ENUM('Pendiente', 'En Proceso', 'Finalizado'),
    FOREIGN KEY (vehiculo_id) REFERENCES Vehiculos(vehiculo_id),
    FOREIGN KEY (proceso_id) REFERENCES Procesos(proceso_id)
);

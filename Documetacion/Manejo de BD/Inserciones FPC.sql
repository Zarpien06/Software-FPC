USE FULLPAINTT;

-- Inserciones

-- TABLE roles
INSERT INTO roles (nombre) VALUES ('admin'), ('empleado'), ('cliente');

-- TABLE tipos_identificacion
INSERT INTO tipos_identificacion (tipo_id, descripcion) VALUES 
('cc', 'Cédula de Ciudadanía'),
('ti', 'Tarjeta de Identidad'),
('ce', 'Cédula de Extranjería'),
('pp', 'Pasaporte'),
-- Nuevos
('nit', 'Numero de identificacion tributaria'),
('pep', 'Permiso Especial de Permanencia');

-- TABLE estados_vehiculo
INSERT INTO estados_vehiculo (estado_id, descripcion) VALUES 
('sin_servicio', 'Sin servicio'),
('en_servicio', 'En servicio'),
('finalizado', 'Finalizado');

-- TABLE tipos_vehiculo
-- Insertar tipos comunes de vehículos
INSERT INTO tipos_vehiculo (nombre) VALUES 
('Sedan'), ('SUV'), ('Hatchback'), ('Pickup'), ('Deportivo'), ('Furgoneta'), ('Camión');

-- TABLE marcas_vehiculo
-- Insertar marcas comunes
INSERT INTO marcas_vehiculo (nombre) VALUES 
('Toyota'), ('Honda'), ('Chevrolet'), ('Ford'), ('Nissan'), ('Mazda'), ('Renault'), ('Volkswagen');

-- TABLE colores
-- Insertar colores comunes
INSERT INTO colores (nombre) VALUES 
('Blanco'), ('Negro'), ('Gris'), ('Plata'), ('Rojo'), ('Azul'), ('Verde'), ('Amarillo');

-- TABLE categorias_servicio
-- Insertar categorías básicas
INSERT INTO categorias_servicio (nombre, descripcion) VALUES
('Pintura', 'Servicios relacionados con la pintura del vehículo'),
('Limpieza', 'Servicios de limpieza y mantenimiento estético'),
('Restauración', 'Servicios de reparación y restauración'),
('Protección', 'Servicios de protección para la carrocería');

-- Tabla de servicios (Normalizada)
-- TABLE servicios
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

-- TABLE estados_cotizacion
INSERT INTO estados_cotizacion (estado_id, descripcion) VALUES 
('pendiente', 'Pendiente de revisión'),
('aceptada', 'Aceptada por el cliente'),
('rechazada', 'Rechazada por el cliente');

-- TABLE estados_reserva
INSERT INTO estados_reserva (estado_id, descripcion) VALUES 
('pendiente', 'Pendiente de inicio'),
('en_proceso', 'En proceso de servicio'),
('completada', 'Servicio completado'),
('cancelada', 'Servicio cancelado');

INSERT INTO estados_proceso (estado_id, descripcion) VALUES 
('en_espera', 'En espera de inicio'),
('en_proceso', 'En proceso de ejecución'),
('terminado', 'Proceso terminado');

-- TABLE tipos_reporte
INSERT INTO tipos_reporte (tipo_id, descripcion) VALUES 
('ingreso', 'Reporte de ingreso de vehículo'),
('proceso', 'Reporte durante el proceso de servicio'),
('salida', 'Reporte de salida y entrega');

-- TABLE tipos_archivo
INSERT INTO tipos_archivo (tipo_id, descripcion) VALUES 
('imagen', 'Archivo de imagen'),
('video', 'Archivo de video'),
('pdf', 'Documento PDF'),
('audio', 'Archivo de audio');

-- TABLE tipos_mensaje 
INSERT INTO tipos_mensaje (tipo_id, descripcion) VALUES 
('texto', 'Mensaje de texto'),
('imagen', 'Archivo de imagen'),
('audio', 'Archivo de audio'),
('archivo', 'Otro tipo de archivo');
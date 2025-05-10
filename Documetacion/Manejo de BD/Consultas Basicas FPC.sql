USE FULLPAINTT;

-- DESDE LA LINEA 4 HASTA LA 35 SON CONSULTAS BASICAS HECHAS POR RONNY
-- Consulta los usuarios que esten activos y con un rol asignado
SELECT * FROM usuarios 
WHERE estado = 'activo' AND rol_id IS NOT NULL;

-- Lista de usuarios ordenados por fecha de registro, lo mas recientes van de primeros
SELECT * FROM usuarios 
ORDER BY fecha_registro DESC;

-- Servicios ordenados por precio de menor a mayor
SELECT * FROM servicios 
ORDER BY precio ASC;

-- Mostrar los 10 servicios mas caros
SELECT * FROM servicios 
ORDER BY precio DESC 
LIMIT 10;

-- Mostrar los últimos 6 vehículos registrados
SELECT * FROM vehiculos 
ORDER BY fecha_registro DESC 
LIMIT 6;

-- servicios que hayan costado entre $50.000 & $200.000
SELECT * FROM servicios 
WHERE precio BETWEEN 50000 AND 200000;
 
-- Calificaciones entre 1 y 3 estrellas
SELECT * FROM calificaciones
WHERE puntuacion BETWEEN 1 AND 3;

-- Calcular el promedio de precios de todos los servicios:
SELECT AVG(precio) AS promedio_precio FROM servicios;

-- Seleccionar un registro específico por ID
SELECT * FROM Usuarios WHERE usuario_id = 1;
SELECT * FROM Clientes WHERE cliente_id = 5;
SELECT * FROM Vehiculos WHERE vehiculo_id = 10;
SELECT * FROM Servicios WHERE servicio_id = 2;
SELECT * FROM Facturas WHERE factura_id = 8;

-- Filtrar por una condición
SELECT * FROM Usuarios WHERE email = 'usuario@correo.com';
SELECT * FROM Clientes WHERE direccion LIKE '%Ciudad A%';
SELECT * FROM Vehiculos WHERE tipo_vehiculo = 'Carro';
SELECT * FROM Servicios WHERE precio > 100.00;
SELECT * FROM Facturas WHERE total < 500.00;

-- Ordenar los resultados
SELECT * FROM Usuarios ORDER BY fecha_registro DESC;
SELECT * FROM Facturas ORDER BY total DESC;
SELECT * FROM Vehiculos ORDER BY año DESC;

-- Contar registros
SELECT COUNT(*) FROM Usuarios;
SELECT COUNT(*) FROM Clientes;
SELECT COUNT(*) FROM Vehiculos;

-- Obtener los últimos registros ingresados
SELECT * FROM Facturas ORDER BY fecha DESC LIMIT 5;
SELECT * FROM Historial_Servicios ORDER BY fecha DESC LIMIT 5;
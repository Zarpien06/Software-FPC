-- 1. Obtener información completa de los clientes, incluyendo su usuario y vehículo
SELECT c.cliente_id, u.nombre AS nombre_cliente, u.email, c.direccion, c.telefono, v.placa, v.marca, v.modelo, v.año
FROM Clientes c
INNER JOIN Usuarios u ON c.usuario_id = u.usuario_id
LEFT JOIN Vehiculos v ON c.cliente_id = v.cliente_id;

-- 2. Obtener todas las facturas con detalles de los servicios comprados
SELECT f.factura_id, u.nombre AS cliente, f.fecha, df.servicio_id, s.nombre AS servicio, df.cantidad, df.precio_unitario, df.total
FROM Facturas f
INNER JOIN Clientes c ON f.cliente_id = c.cliente_id
INNER JOIN Usuarios u ON c.usuario_id = u.usuario_id
INNER JOIN Detalle_Factura df ON f.factura_id = df.factura_id
INNER JOIN Servicios s ON df.servicio_id = s.servicio_id;

-- 3. Obtener el historial de servicios realizados con detalles del vehículo y el empleado responsable
SELECT hs.historial_id, v.placa, v.marca, v.modelo, u.nombre AS cliente, s.nombre AS servicio, hs.fecha, hs.costo, e.empleado_id, ue.nombre AS empleado
FROM Historial_Servicios hs
INNER JOIN Vehiculos v ON hs.vehiculo_id = v.vehiculo_id
INNER JOIN Clientes c ON v.cliente_id = c.cliente_id
INNER JOIN Usuarios u ON c.usuario_id = u.usuario_id
INNER JOIN Servicios s ON hs.servicio_id = s.servicio_id
LEFT JOIN Asignacion_Empleados_Servicios aes ON hs.historial_id = aes.historial_id
LEFT JOIN Empleados e ON aes.empleado_id = e.empleado_id
LEFT JOIN Usuarios ue ON e.usuario_id = ue.usuario_id;

-- 4. Obtener todos los empleados y los procesos en los que están involucrados
SELECT e.empleado_id, ue.nombre AS empleado, p.proceso_id, tp.nombre AS tipo_proceso, p.estado, p.fecha_inicio, p.fecha_fin
FROM Empleados e
INNER JOIN Usuarios ue ON e.usuario_id = ue.usuario_id
LEFT JOIN Procesos p ON e.empleado_id = p.empleado_id
LEFT JOIN Tipos_Proceso tp ON p.tipo_proceso_id = tp.tipo_proceso_id;

-- 5. Obtener los clientes con o sin vehículos registrados
SELECT u.nombre AS cliente, c.direccion, c.telefono, v.placa, v.marca, v.modelo
FROM Clientes c
LEFT JOIN Usuarios u ON c.usuario_id = u.usuario_id
LEFT JOIN Vehiculos v ON c.cliente_id = v.cliente_id;

-- 6. Obtener los empleados y los servicios asignados a ellos (incluyendo empleados sin asignaciones)
SELECT e.empleado_id, u.nombre AS empleado, s.nombre AS servicio, hs.fecha, hs.costo
FROM Empleados e
INNER JOIN Usuarios u ON e.usuario_id = u.usuario_id
LEFT JOIN Asignacion_Empleados_Servicios aes ON e.empleado_id = aes.empleado_id
LEFT JOIN Historial_Servicios hs ON aes.historial_id = hs.historial_id
LEFT JOIN Servicios s ON hs.servicio_id = s.servicio_id;

-- 7. Obtener todos los procesos con detalles de los vehículos y empleados
SELECT p.proceso_id, v.placa, tp.nombre AS tipo_proceso, e.empleado_id, ue.nombre AS empleado, p.estado, p.fecha_inicio, p.fecha_fin
FROM Procesos p
INNER JOIN Vehiculos v ON p.vehiculo_id = v.vehiculo_id
INNER JOIN Tipos_Proceso tp ON p.tipo_proceso_id = tp.tipo_proceso_id
INNER JOIN Empleados e ON p.empleado_id = e.empleado_id
INNER JOIN Usuarios ue ON e.usuario_id = ue.usuario_id;

-- 8. Obtener todas las facturas y verificar si los clientes han realizado compras o no (FULL OUTER JOIN simulado con UNION)
SELECT u.nombre AS cliente, f.factura_id, f.fecha, f.total
FROM Clientes c
LEFT JOIN Usuarios u ON c.usuario_id = u.usuario_id
LEFT JOIN Facturas f ON c.cliente_id = f.cliente_id
UNION
SELECT u.nombre AS cliente, f.factura_id, f.fecha, f.total
FROM Clientes c
RIGHT JOIN Usuarios u ON c.usuario_id = u.usuario_id
RIGHT JOIN Facturas f ON c.cliente_id = f.cliente_id;

-- 9. Obtener todos los empleados con procesos asignados y mostrar los que no tienen procesos (RIGHT JOIN)
SELECT e.empleado_id, u.nombre AS empleado, p.proceso_id, tp.nombre AS tipo_proceso, p.estado
FROM Procesos p
RIGHT JOIN Empleados e ON p.empleado_id = e.empleado_id
RIGHT JOIN Usuarios u ON e.usuario_id = u.usuario_id
LEFT JOIN Tipos_Proceso tp ON p.tipo_proceso_id = tp.tipo_proceso_id;

-- 10. Obtener un resumen de cuántos vehículos tiene cada cliente
SELECT u.nombre AS cliente, COUNT(v.vehiculo_id) AS cantidad_vehiculos
FROM Clientes c
INNER JOIN Usuarios u ON c.usuario_id = u.usuario_id
LEFT JOIN Vehiculos v ON c.cliente_id = v.cliente_id
GROUP BY u.nombre;

-- 11. Obtener los 5 servicios más costosos realizados en la empresa
SELECT s.nombre AS servicio, AVG(hs.costo) AS costo_promedio
FROM Historial_Servicios hs
INNER JOIN Servicios s ON hs.servicio_id = s.servicio_id
GROUP BY s.nombre
ORDER BY costo_promedio DESC
LIMIT 5;

-- 12. Obtener la cantidad de facturas emitidas por cada cliente
SELECT u.nombre AS cliente, COUNT(f.factura_id) AS total_facturas
FROM Facturas f
INNER JOIN Clientes c ON f.cliente_id = c.cliente_id
INNER JOIN Usuarios u ON c.usuario_id = u.usuario_id
GROUP BY u.nombre;

-- 13. Obtener los servicios que han sido asignados a empleados junto con los que no tienen asignación
SELECT s.servicio_id, s.nombre AS servicio, e.empleado_id, u.nombre AS empleado
FROM Servicios s
LEFT JOIN Historial_Servicios hs ON s.servicio_id = hs.servicio_id
LEFT JOIN Asignacion_Empleados_Servicios aes ON hs.historial_id = aes.historial_id
LEFT JOIN Empleados e ON aes.empleado_id = e.empleado_id
LEFT JOIN Usuarios u ON e.usuario_id = u.usuario_id;

-- 14. Obtener los empleados que han trabajado en más procesos
SELECT u.nombre AS empleado, COUNT(p.proceso_id) AS total_procesos
FROM Empleados e
INNER JOIN Usuarios u ON e.usuario_id = u.usuario_id
LEFT JOIN Procesos p ON e.empleado_id = p.empleado_id
GROUP BY u.nombre
ORDER BY total_procesos DESC
LIMIT 5;

-- 15. Obtener los clientes que han tenido más servicios en el taller
SELECT u.nombre AS cliente, COUNT(hs.historial_id) AS total_servicios
FROM Clientes c
INNER JOIN Usuarios u ON c.usuario_id = u.usuario_id
LEFT JOIN Vehiculos v ON c.cliente_id = v.cliente_id
LEFT JOIN Historial_Servicios hs ON v.vehiculo_id = hs.vehiculo_id
GROUP BY u.nombre
ORDER BY total_servicios DESC
LIMIT 5;

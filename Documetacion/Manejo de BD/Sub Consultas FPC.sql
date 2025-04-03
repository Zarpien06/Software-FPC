-- Sub Consultas 

-- 1. Subconsulta en SELECT: Cantidad de vehículos por cliente
SELECT 
    c.cliente_id,
    u.nombre AS cliente_nombre,
    (SELECT COUNT(*) FROM Vehiculos v WHERE v.cliente_id = c.cliente_id) AS total_vehiculos
FROM Clientes c
JOIN Usuarios u ON c.usuario_id = u.usuario_id;

-- 2. Subconsulta en FROM: Empleados con más de un servicio asignado
SELECT e.empleado_id, u.nombre, subq.total_servicios
FROM Empleados e
JOIN Usuarios u ON e.usuario_id = u.usuario_id
JOIN (
    SELECT empleado_id, COUNT(*) AS total_servicios
    FROM Asignacion_Empleados_Servicios
    GROUP BY empleado_id
    HAVING total_servicios > 1
) subq ON e.empleado_id = subq.empleado_id;

-- 3. Subconsulta en WHERE: Vehículos de clientes con más de 2 servicios
SELECT * 
FROM Vehiculos v
WHERE v.cliente_id IN (
    SELECT cliente_id 
    FROM Historial_Servicios hs
    JOIN Vehiculos vh ON hs.vehiculo_id = vh.vehiculo_id
    GROUP BY cliente_id
    HAVING COUNT(*) > 2
);

-- 4. Subconsulta en HAVING: Clientes que han gastado más de 1000 en facturas
SELECT c.cliente_id, u.nombre, SUM(f.total) AS total_gastado
FROM Clientes c
JOIN Usuarios u ON c.usuario_id = u.usuario_id
JOIN Facturas f ON c.cliente_id = f.cliente_id
GROUP BY c.cliente_id, u.nombre
HAVING total_gastado > 1000;

-- 5. Subconsulta correlacionada: Facturas con el total más alto por cliente
SELECT f.factura_id, f.cliente_id, f.total
FROM Facturas f
WHERE f.total = (
    SELECT MAX(f2.total) 
    FROM Facturas f2 
    WHERE f2.cliente_id = f.cliente_id
);

-- 6. Subconsulta en INSERT: Agregar empleado con usuario más reciente
INSERT INTO Empleados (usuario_id, puesto, telefono)
VALUES (
    (SELECT usuario_id FROM Usuarios ORDER BY fecha_registro DESC LIMIT 1), 
    'Mecánico', 
    '1234567890'
);

-- 7. Subconsulta en UPDATE: Finalizar procesos si el último mantenimiento fue hace más de 6 meses
UPDATE Procesos
SET estado = 'Finalizado'
WHERE vehiculo_id IN (
    SELECT vehiculo_id FROM Registro_Mantenimiento
    WHERE fecha < DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
);

-- 8. Subconsulta en DELETE: Eliminar clientes sin facturas
DELETE FROM Clientes 
WHERE cliente_id NOT IN (SELECT cliente_id FROM Facturas);

-- 9. Subconsulta con EXISTS: Clientes con al menos un vehículo
SELECT c.cliente_id, u.nombre
FROM Clientes c
JOIN Usuarios u ON c.usuario_id = u.usuario_id
WHERE EXISTS (
    SELECT 1 FROM Vehiculos v WHERE v.cliente_id = c.cliente_id
);

-- 10. Subconsulta con NOT EXISTS: Empleados sin servicios asignados
SELECT e.empleado_id, u.nombre
FROM Empleados e
JOIN Usuarios u ON e.usuario_id = u.usuario_id
WHERE NOT EXISTS (
    SELECT 1 FROM Asignacion_Empleados_Servicios aes WHERE aes.empleado_id = e.empleado_id
);

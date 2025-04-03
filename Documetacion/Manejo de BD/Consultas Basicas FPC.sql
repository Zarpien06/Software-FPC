-- Consultas basicas

-- Seleccionar todos los registros de cada tabla
SELECT * FROM Roles;
SELECT * FROM Usuarios;
SELECT * FROM Clientes;
SELECT * FROM Empleados;
SELECT * FROM Administradores;
SELECT * FROM Vehiculos;
SELECT * FROM Servicios;
SELECT * FROM Historial_Servicios;
SELECT * FROM Facturas;
SELECT * FROM Detalle_Factura;
SELECT * FROM Tipos_Proceso;
SELECT * FROM Procesos;
SELECT * FROM Registro_Mantenimiento;
SELECT * FROM Historial_Cliente;
SELECT * FROM Historial_Servicios_Realizados;
SELECT * FROM Asignacion_Proceso_Vehiculo;

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

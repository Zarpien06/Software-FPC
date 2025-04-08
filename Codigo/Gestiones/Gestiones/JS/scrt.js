// Variables globales
let procesos = [
    {
        id: 'PRO-001',
        vehiculo: 'Toyota Corolla (ABC-123)',
        idVehiculo: 1,
        tipo: 'Mantenimiento preventivo',
        tipoId: 'mantenimiento_preventivo',
        descripcion: 'Cambio de aceite y filtros',
        fecha: '2025-04-05',
        fechaFin: '2025-04-05',
        estado: 'completado',
        kilometraje: 45000,
        notas: 'Cliente solicitó revisión de frenos adicional'
    },
    {
        id: 'PRO-002',
        vehiculo: 'Honda Civic (DEF-456)',
        idVehiculo: 2,
        tipo: 'Reparación',
        tipoId: 'reparacion',
        descripcion: 'Sustitución de frenos delanteros',
        fecha: '2025-04-06',
        fechaFin: '2025-04-07',
        estado: 'activo',
        kilometraje: 78000,
        notas: ''
    },
    {
        id: 'PRO-003',
        vehiculo: 'Ford F-150 (GHI-789)',
        idVehiculo: 3,
        tipo: 'Inspección',
        tipoId: 'inspeccion',
        descripcion: 'Revisión general de sistemas',
        fecha: '2025-04-08',
        fechaFin: '2025-04-08',
        estado: 'programado',
        kilometraje: 32000,
        notas: 'Especial atención al sistema de suspensión'
    },
    {
        id: 'PRO-004',
        vehiculo: 'Chevrolet Cruze (JKL-012)',
        idVehiculo: 4,
        tipo: 'Mantenimiento correctivo',
        tipoId: 'mantenimiento_correctivo',
        descripcion: 'Reparación sistema eléctrico',
        fecha: '2025-04-03',
        fechaFin: '2025-04-04',
        estado: 'urgente',
        kilometraje: 65000,
        notas: 'Fallo en el alternador'
    },
    {
        id: 'PRO-005',
        vehiculo: 'Nissan Sentra (MNO-345)',
        idVehiculo: 5,
        tipo: 'Mantenimiento preventivo',
        tipoId: 'mantenimiento_preventivo',
        descripcion: 'Alineación y balanceo',
        fecha: '2025-04-10',
        fechaFin: '2025-04-10',
        estado: 'programado',
        kilometraje: 28000,
        notas: ''
    },
];

// DOM Elements
const btnNuevoProceso = document.getElementById('btnNuevoProceso');
const procesoModal = document.getElementById('procesoModal');
const confirmDeleteModal = document.getElementById('confirmDeleteModal');
const btnCancelar = document.getElementById('btnCancelar');
const btnCancelarDelete = document.getElementById('btnCancelarDelete');
const btnConfirmarDelete = document.getElementById('btnConfirmarDelete');
const formProceso = document.getElementById('formProceso');
const tablaProcesos = document.getElementById('tablaProcesos');
const filtroEstado = document.getElementById('filtroEstado');
const filtroFecha = document.getElementById('filtroFecha');
const filtroVehiculo = document.getElementById('filtroVehiculo');
const closeBtns = document.querySelectorAll('.close-modal');

// Variables para edición
let editandoProceso = false;
let procesoIdActual = null;

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    cargarTabla();
    inicializarEventos();
});

function inicializarEventos() {
    // Botón nuevo proceso
    btnNuevoProceso.addEventListener('click', () => {
        abrirModalCrear();
    });

    // Cerrar modales
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            cerrarModales();
        });
    });

    // Botones cancelar
    btnCancelar.addEventListener('click', () => {
        cerrarModales();
    });

    btnCancelarDelete.addEventListener('click', () => {
        cerrarModales();
    });

    // Envío del formulario
    formProceso.addEventListener('submit', (e) => {
        e.preventDefault();
        guardarProceso();
    });

    // Fuera del modal para cerrar
    window.addEventListener('click', (e) => {
        if (e.target === procesoModal || e.target === confirmDeleteModal) {
            cerrarModales();
        }
    });

    // Filtros
    filtroEstado.addEventListener('change', cargarTabla);
    filtroFecha.addEventListener('change', cargarTabla);
    filtroVehiculo.addEventListener('change', cargarTabla);

    // Botón confirmar eliminación
    btnConfirmarDelete.addEventListener('click', eliminarProcesoConfirmado);
}

// Funciones principales

function cargarTabla() {
    const estado = filtroEstado.value;
    const fecha = filtroFecha.value;
    const vehiculo = filtroVehiculo.value;
    
    // Filtrar procesos según los criterios seleccionados
    let procesosFiltrados = [...procesos];
    
    if (estado !== 'todos') {
        procesosFiltrados = procesosFiltrados.filter(proceso => proceso.estado === estado);
    }
    
    if (fecha) {
        procesosFiltrados = procesosFiltrados.filter(proceso => proceso.fecha === fecha);
    }
    
    if (vehiculo !== 'todos') {
        procesosFiltrados = procesosFiltrados.filter(proceso => proceso.idVehiculo.toString() === vehiculo);
    }
    
    // Generar filas de la tabla
    tablaProcesos.innerHTML = '';
    
    if (procesosFiltrados.length === 0) {
        tablaProcesos.innerHTML = `
            <tr>
                <td colspan="7" class="empty-table">No se encontraron procesos con los filtros seleccionados</td>
            </tr>
        `;
        return;
    }
    
    procesosFiltrados.forEach(proceso => {
        const fila = document.createElement('tr');
        
        // Determinar la clase del badge según el estado
        let badgeClass;
        switch (proceso.estado) {
            case 'activo':
                badgeClass = 'badge-active';
                estadoTexto = 'En progreso';
                break;
            case 'completado':
                badgeClass = 'badge-completed';
                estadoTexto = 'Completado';
                break;
            case 'programado':
                badgeClass = 'badge-scheduled';
                estadoTexto = 'Programado';
                break;
            case 'urgente':
                badgeClass = 'badge-urgent';
                estadoTexto = 'Urgente';
                break;
            default:
                badgeClass = '';
                estadoTexto = proceso.estado;
        }
        
        fila.innerHTML = `
            <td>#${proceso.id}</td>
            <td>${proceso.vehiculo}</td>
            <td>${proceso.tipo}</td>
            <td>${proceso.descripcion}</td>
            <td>${formatearFecha(proceso.fecha)}</td>
            <td><span class="${badgeClass}">${estadoTexto}</span></td>
            <td class="actions">
                <button class="btn-view" title="Ver detalle" data-id="${proceso.id}"><i class="fas fa-eye"></i></button>
                <button class="btn-edit" title="Editar" data-id="${proceso.id}"><i class="fas fa-edit"></i></button>
                <button class="btn-delete" title="Eliminar" data-id="${proceso.id}"><i class="fas fa-trash"></i></button>
            </td>
        `;
        
        tablaProcesos.appendChild(fila);
    });
    
    // Agregar event listeners a los botones de acción
    document.querySelectorAll('.btn-view').forEach(btn => {
        btn.addEventListener('click', () => verProceso(btn.dataset.id));
    });
    
    document.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', () => editarProceso(btn.dataset.id));
    });
    
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', () => confirmarEliminarProceso(btn.dataset.id));
    });
}

function abrirModalCrear() {
    // Limpiar el formulario
    formProceso.reset();
    
    // Establecer fecha actual por defecto
    const fechaActual = new Date().toISOString().split('T')[0];
    document.getElementById('fechaInicio').value = fechaActual;
    
    // Cambiar título del modal
    document.getElementById('modalTitle').textContent = 'Nuevo Proceso';
    
    // Reiniciar variables de edición
    editandoProceso = false;
    procesoIdActual = null;
    
    // Abrir el modal
    procesoModal.classList.add('active');
}

function editarProceso(id) {
    // Buscar el proceso por ID
    const proceso = procesos.find(p => p.id === id);
    
    if (!proceso) return;
    
    // Llenar el formulario con los datos del proceso
    document.getElementById('vehiculo').value = proceso.idVehiculo;
    document.getElementById('tipoProceso').value = proceso.tipoId;
    document.getElementById('descripcion').value = proceso.descripcion;
    document.getElementById('fechaInicio').value = proceso.fecha;
    document.getElementById('fechaFin').value = proceso.fechaFin;
    document.getElementById('estado').value = proceso.estado;
    document.getElementById('kilometraje').value = proceso.kilometraje;
    document.getElementById('notas').value = proceso.notas;
    
    // Cambiar título del modal
    document.getElementById('modalTitle').textContent = 'Editar Proceso';
    
    // Establecer variables de edición
    editandoProceso = true;
    procesoIdActual = id;
    
    // Abrir el modal
    procesoModal.classList.add('active');
}

function verProceso(id) {
    // Buscar el proceso por ID
    const proceso = procesos.find(p => p.id === id);
    
    if (!proceso) return;
    
    // Llenar el formulario con los datos del proceso (solo lectura)
    document.getElementById('vehiculo').value = proceso.idVehiculo;
    document.getElementById('tipoProceso').value = proceso.tipoId;
    document.getElementById('descripcion').value = proceso.descripcion;
    document.getElementById('fechaInicio').value = proceso.fecha;
    document.getElementById('fechaFin').value = proceso.fechaFin;
    document.getElementById('estado').value = proceso.estado;
    document.getElementById('kilometraje').value = proceso.kilometraje;
    document.getElementById('notas').value = proceso.notas;
    
    // Deshabilitar campos
    toggleCamposFormulario(true);
    
    // Cambiar título del modal
    document.getElementById('modalTitle').textContent = 'Ver Detalle de Proceso';
    
    // Ocultar botón guardar
    document.getElementById('btnGuardar').style.display = 'none';
    
    // Cambiar texto del botón cancelar
    document.getElementById('btnCancelar').textContent = 'Cerrar';
    
    // Abrir el modal
    procesoModal.classList.add('active');
}

function confirmarEliminarProceso(id) {
    // Guardar ID del proceso a eliminar
    procesoIdActual = id;
    
    // Abrir modal de confirmación
    confirmDeleteModal.classList.add('active');
}

function eliminarProcesoConfirmado() {
    if (!procesoIdActual) return;
    
    // Eliminar proceso del array
    procesos = procesos.filter(p => p.id !== procesoIdActual);
    
    // Actualizar tabla
    cargarTabla();
    
    // Cerrar modal
    cerrarModales();
    
    // Mostrar notificación
    mostrarNotificacion('Proceso eliminado correctamente', 'success');
}

function guardarProceso() {
    // Obtener valores del formulario
    const idVehiculo = document.getElementById('vehiculo').value;
    const tipoProcesoId = document.getElementById('tipoProceso').value;
    const descripcion = document.getElementById('descripcion').value;
    const fechaInicio = document.getElementById('fechaInicio').value;
    const fechaFin = document.getElementById('fechaFin').value;
    const estado = document.getElementById('estado').value;
    const kilometraje = document.getElementById('kilometraje').value;
    const notas = document.getElementById('notas').value;
    
    // Validar campos requeridos
    if (!idVehiculo || !tipoProcesoId || !descripcion || !fechaInicio || !estado) {
        mostrarNotificacion('Por favor complete todos los campos requeridos', 'error');
        return;
    }
    
    // Obtener información adicional
    const vehiculoSeleccionado = document.getElementById('vehiculo').options[document.getElementById('vehiculo').selectedIndex].text;
    const tipoProcesoTexto = document.getElementById('tipoProceso').options[document.getElementById('tipoProceso').selectedIndex].text;
    
    // Crear objeto de proceso
    const procesoDatos = {
        vehiculo: vehiculoSeleccionado,
        idVehiculo: parseInt(idVehiculo),
        tipo: tipoProcesoTexto,
        tipoId: tipoProcesoId,
        descripcion: descripcion,
        fecha: fechaInicio,
        fechaFin: fechaFin || fechaInicio,
        estado: estado,
        kilometraje: kilometraje ? parseInt(kilometraje) : 0,
        notas: notas
    };
    
    if (editandoProceso) {
        // Actualizar proceso existente
        const index = procesos.findIndex(p => p.id === procesoIdActual);
        if (index !== -1) {
            procesoDatos.id = procesoIdActual;
            procesos[index] = procesoDatos;
            mostrarNotificacion('Proceso actualizado correctamente', 'success');
        }
    } else {
        // Crear nuevo proceso con ID incremental
        const ultimoId = procesos.length > 0 ? 
            parseInt(procesos[procesos.length - 1].id.replace('PRO-', '')) : 0;
        const nuevoId = `PRO-${String(ultimoId + 1).padStart(3, '0')}`;
        
        procesoDatos.id = nuevoId;
        procesos.push(procesoDatos);
        mostrarNotificacion('Proceso creado correctamente', 'success');
    }
    
    // Actualizar tabla y cerrar modal
    cargarTabla();
    cerrarModales();
    
    // Restablecer formulario
    habilitarFormulario();
}

// Funciones auxiliares

function cerrarModales() {
    // Cerrar todos los modales
    procesoModal.classList.remove('active');
    confirmDeleteModal.classList.remove('active');
    
    // Restablecer formulario
    habilitarFormulario();
}

function habilitarFormulario() {
    // Habilitar campos
    toggleCamposFormulario(false);
    
    // Mostrar botón guardar
    document.getElementById('btnGuardar').style.display = 'block';
    
    // Restablecer texto del botón cancelar
    document.getElementById('btnCancelar').textContent = 'Cancelar';
}

function toggleCamposFormulario(deshabilitado) {
    // Habilitar/deshabilitar todos los campos del formulario
    document.getElementById('vehiculo').disabled = deshabilitado;
    document.getElementById('tipoProceso').disabled = deshabilitado;
    document.getElementById('descripcion').disabled = deshabilitado;
    document.getElementById('fechaInicio').disabled = deshabilitado;
    document.getElementById('fechaFin').disabled = deshabilitado;
    document.getElementById('estado').disabled = deshabilitado;
    document.getElementById('kilometraje').disabled = deshabilitado;
    document.getElementById('notas').disabled = deshabilitado;
}

function formatearFecha(fechaStr) {
    if (!fechaStr) return '';
    
    const fecha = new Date(fechaStr);
    return fecha.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

function mostrarNotificacion(mensaje, tipo) {
    // Crear elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion ${tipo}`;
    
    // Icono según tipo
    let icono = '';
    switch (tipo) {
        case 'success':
            icono = '<i class="fas fa-check-circle"></i>';
            break;
        case 'error':
            icono = '<i class="fas fa-times-circle"></i>';
            break;
        case 'warning':
            icono = '<i class="fas fa-exclamation-circle"></i>';
            break;
        default:
            icono = '<i class="fas fa-info-circle"></i>';
    }
    
    notificacion.innerHTML = `
        ${icono}
        <span>${mensaje}</span>
    `;
    
    // Agregar al DOM
    document.body.appendChild(notificacion);
    
    // Mostrar notificación con animación
    setTimeout(() => {
        notificacion.classList.add('show');
    }, 10);
    
    // Eliminar después de 3 segundos
    setTimeout(() => {
        notificacion.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notificacion);
        }, 300);
    }, 3000);
}

// Agregar estilos para notificaciones
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    .notificacion {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 16px;
        border-radius: 8px;
        background-color: white;
        color: var(--dark);
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        transform: translateX(120%);
        transition: transform 0.3s ease;
        z-index: 1000;
        max-width: 350px;
    }
    
    .notificacion.show {
        transform: translateX(0);
    }
    
    .notificacion i {
        font-size: 18px;
    }
    
    .notificacion.success i {
        color: var(--success-color);
    }
    
    .notificacion.error i {
        color: var(--danger-color);
    }
    
    .notificacion.warning i {
        color: var(--warning-color);
    }
    
    .notificacion.info i {
        color: var(--primary-color);
    }
    
    .empty-table {
        text-align: center;
        padding: 40px 0;
        color: var(--gray-dark);
        font-style: italic;
    }
`;

document.head.appendChild(notificationStyle);
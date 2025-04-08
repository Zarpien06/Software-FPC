// Variables para elementos DOM
const newReportBtn = document.getElementById('btnNewReport');
const reportModal = document.getElementById('reportModal');
const deleteModal = document.getElementById('deleteModal');
const closeModalBtn = document.getElementById('closeModal');
const closeDeleteModalBtn = document.getElementById('closeDeleteModal');
const cancelReportBtn = document.getElementById('cancelReport');
const cancelDeleteBtn = document.getElementById('cancelDelete');
const confirmDeleteBtn = document.getElementById('confirmDelete');
const reportForm = document.getElementById('reportForm');
const modalTitle = document.getElementById('modalTitle');
const applyFiltersBtn = document.getElementById('btnApplyFilters');
const filterDate = document.getElementById('filterDate');
const filterStatus = document.getElementById('filterStatus');
const filterType = document.getElementById('filterType');

// Variables para gestión de reportes
let currentReportId = null;
let reports = [
    {
        id: 'REP-2025042',
        client: 'Carlos Ramírez',
        vehicle: 'Toyota Corolla 2022',
        type: 'Pintura completa',
        date: '05/04/2025',
        status: 'completed'
    },
    {
        id: 'REP-2025041',
        client: 'María González',
        vehicle: 'Honda Civic 2023',
        type: 'Reparación de chapa',
        date: '04/04/2025',
        status: 'in-progress'
    },
    {
        id: 'REP-2025040',
        client: 'Juan Pérez',
        vehicle: 'Ford Mustang 2020',
        type: 'Detailing premium',
        date: '03/04/2025',
        status: 'completed'
    },
    {
        id: 'REP-2025039',
        client: 'Elena Martínez',
        vehicle: 'Nissan Sentra 2021',
        type: 'Cambio de color',
        date: '03/04/2025',
        status: 'pending'
    },
    {
        id: 'REP-2025038',
        client: 'Fernando López',
        vehicle: 'Chevrolet Camaro 2019',
        type: 'Pintado parcial',
        date: '02/04/2025',
        status: 'completed'
    },
    {
        id: 'REP-2025037',
        client: 'Laura Torres',
        vehicle: 'Hyundai Elantra 2022',
        type: 'Reparación de golpe',
        date: '01/04/2025',
        status: 'in-progress'
    }
];

// Abrir modal para nuevo reporte
newReportBtn.addEventListener('click', () => {
    openReportModal();
});

// Cerrar modales
closeModalBtn.addEventListener('click', () => {
    closeReportModal();
});

closeDeleteModalBtn.addEventListener('click', () => {
    closeDeleteModal();
});

cancelReportBtn.addEventListener('click', () => {
    closeReportModal();
});

cancelDeleteBtn.addEventListener('click', () => {
    closeDeleteModal();
});

// Función para abrir modal de reporte (nuevo o editar)
function openReportModal(reportId = null) {
    currentReportId = reportId;
    
    if (reportId) {
        // Modo edición
        const report = reports.find(r => r.id === reportId);
        if (report) {
            modalTitle.textContent = 'Editar Reporte';
            
            // Llenar formulario con datos del reporte
            document.getElementById('clientName').value = report.client;
            
            // Extraer modelo y año del vehículo
            const vehicleInfo = report.vehicle.split(' ');
            const year = vehicleInfo.pop();
            const model = vehicleInfo.join(' ');
            
            document.getElementById('vehicleModel').value = model;
            document.getElementById('vehicleYear').value = year;
            
            // Mapear tipo de servicio al valor del select
            const serviceTypeMap = {
                'Pintura completa': 'paint',
                'Pintado parcial': 'partial',
                'Reparación de chapa': 'repair',
                'Cambio de color': 'color',
                'Detailing premium': 'detailing',
                'Reparación de golpe': 'repair'
            };
            
            document.getElementById('serviceType').value = serviceTypeMap[report.type] || 'other';
            document.getElementById('reportStatus').value = report.status;
            
            // Valores por defecto para campos adicionales
            document.getElementById('serviceDescription').value = 'Servicio de ' + report.type;
            document.getElementById('observations').value = 'Cliente recurrente. Vehículo en buen estado general.';
        }
    } else {
        // Modo nuevo reporte
        modalTitle.textContent = 'Nuevo Reporte';
        reportForm.reset();
    }
    
    reportModal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Evitar scroll
}

// Función para cerrar modal de reporte
function closeReportModal() {
    reportModal.classList.remove('active');
    document.body.style.overflow = '';
    currentReportId = null;
}

// Función para abrir modal de confirmación de eliminación
function openDeleteModal(reportId) {
    currentReportId = reportId;
    deleteModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Función para cerrar modal de confirmación de eliminación
function closeDeleteModal() {
    deleteModal.classList.remove('active');
    document.body.style.overflow = '';
    currentReportId = null;
}

// Manejador para envío del formulario
reportForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Obtener valores del formulario
    const clientName = document.getElementById('clientName').value;
    const vehicleModel = document.getElementById('vehicleModel').value;
    const vehicleYear = document.getElementById('vehicleYear').value;
    const serviceType = document.getElementById('serviceType');
    const serviceTypeText = serviceType.options[serviceType.selectedIndex].text;
    const status = document.getElementById('reportStatus').value;
    
    // Obtener fecha actual en formato DD/MM/YYYY
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();
    const formattedDate = `${day}/${month}/${year}`;
    
    // Crear objeto de reporte
    const vehicle = `${vehicleModel} ${vehicleYear}`;
    
    if (currentReportId) {
        // Actualizar reporte existente
        const reportIndex = reports.findIndex(r => r.id === currentReportId);
        if (reportIndex !== -1) {
            reports[reportIndex] = {
                ...reports[reportIndex],
                client: clientName,
                vehicle: vehicle,
                type: serviceTypeText,
                status: status
            };
            
            // Actualizar fila en la tabla
            updateReportRow(currentReportId, reports[reportIndex]);
        }
    } else {
        // Generar nuevo ID de reporte
        const nextNumber = reports.length > 0 
            ? parseInt(reports[0].id.split('-')[1]) + 1 
            : 2025001;
        
        const newId = `REP-${nextNumber}`;
        
        // Crear nuevo reporte
        const newReport = {
            id: newId,
            client: clientName,
            vehicle: vehicle,
            type: serviceTypeText,
            date: formattedDate,
            status: status
        };
        
        // Añadir al arreglo de reportes (al inicio para que sea el más reciente)
        reports.unshift(newReport);
        
        // Añadir a la tabla
        addReportRow(newReport);
    }
    
    // Cerrar modal
    closeReportModal();
    
    // Mostrar notificación
    showNotification(currentReportId ? 'Reporte actualizado con éxito' : 'Nuevo reporte creado con éxito');
});

// Función para añadir fila a la tabla de reportes
function addReportRow(report) {
    const tbody = document.querySelector('.reports-table tbody');
    
    // Crear nueva fila
    const row = document.createElement('tr');
    row.setAttribute('data-id', report.id);
    
    // Mapeo de estado a clase de badge
    const statusClassMap = {
        'completed': 'completed',
        'in-progress': 'in-progress',
        'pending': 'pending'
    };
    
    // Mapeo de estado a texto en español
    const statusTextMap = {
        'completed': 'Completado',
        'in-progress': 'En progreso',
        'pending': 'Pendiente'
    };
    
    // Crear contenido de la fila
    row.innerHTML = `
        <td>#${report.id}</td>
        <td>${report.client}</td>
        <td>${report.vehicle}</td>
        <td>${report.type}</td>
        <td>${report.date}</td>
        <td><span class="status-badge ${statusClassMap[report.status]}">${statusTextMap[report.status]}</span></td>
        <td class="action-buttons">
            <button class="btn-view" title="Ver reporte"><i class="fas fa-eye"></i></button>
            <button class="btn-edit" title="Editar reporte"><i class="fas fa-edit"></i></button>
            <button class="btn-delete" title="Eliminar reporte"><i class="fas fa-trash"></i></button>
        </td>
    `;
    
    // Añadir al inicio de la tabla
    if (tbody.firstChild) {
        tbody.insertBefore(row, tbody.firstChild);
    } else {
        tbody.appendChild(row);
    }
    
    // Añadir event listeners a los botones
    attachRowButtonListeners(row);
}

// Función para actualizar fila existente
function updateReportRow(reportId, report) {
    const row = document.querySelector(`.reports-table tbody tr[data-id="${reportId}"]`);
    if (!row) return;
    
    const statusClassMap = {
        'completed': 'completed',
        'in-progress': 'in-progress',
        'pending': 'pending'
    };
    
    const statusTextMap = {
        'completed': 'Completado',
        'in-progress': 'En progreso',
        'pending': 'Pendiente'
    };
    
    // Actualizar celdas de la fila
    row.cells[1].textContent = report.client;
    row.cells[2].textContent = report.vehicle;
    row.cells[3].textContent = report.type;
    
    // Actualizar badge de estado
    const statusBadge = row.cells[5].querySelector('.status-badge');
    statusBadge.className = `status-badge ${statusClassMap[report.status]}`;
    statusBadge.textContent = statusTextMap[report.status];
}

// Función para adjuntar listeners a los botones de cada fila
function attachRowButtonListeners(row) {
    const reportId = row.getAttribute('data-id');
    
    // Botón de ver detalles
    const viewBtn = row.querySelector('.btn-view');
    viewBtn.addEventListener('click', () => {
        // Implementar vista de detalles (puede ser otra modal o página)
        showNotification('Visualizando detalles del reporte #' + reportId);
    });
    
    // Botón de editar
    const editBtn = row.querySelector('.btn-edit');
    editBtn.addEventListener('click', () => {
        openReportModal(reportId);
    });
    
    // Botón de eliminar
    const deleteBtn = row.querySelector('.btn-delete');
    deleteBtn.addEventListener('click', () => {
        openDeleteModal(reportId);
    });
}

// Función para mostrar notificación
function showNotification(message) {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-check-circle"></i>
            <p>${message}</p>
        </div>
    `;
    
    // Añadir al DOM
    document.body.appendChild(notification);
    
    // Añadir estilo del elemento de notificación (se puede mover al CSS)
    notification.style.position = 'fixed';
    notification.style.bottom = '20px';
    notification.style.right = '20px';
    notification.style.backgroundColor = 'var(--primary-color)';
    notification.style.color = 'white';
    notification.style.padding = '15px 20px';
    notification.style.borderRadius = 'var(--border-radius)';
    notification.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    notification.style.zIndex = '1000';
    notification.style.minWidth = '300px';
    notification.style.transform = 'translateY(100px)';
    notification.style.opacity = '0';
    notification.style.transition = 'all 0.3s ease';
    
    // Estilo para el contenido
    const content = notification.querySelector('.notification-content');
    content.style.display = 'flex';
    content.style.alignItems = 'center';
    
    // Estilo para el icono
    const icon = notification.querySelector('i');
    icon.style.fontSize = '24px';
    icon.style.marginRight = '15px';
    
    // Mostrar con animación
    setTimeout(() => {
        notification.style.transform = 'translateY(0)';
        notification.style.opacity = '1';
    }, 10);
    
    // Ocultar después de 3 segundos
    setTimeout(() => {
        notification.style.transform = 'translateY(100px)';
        notification.style.opacity = '0';
        
        // Eliminar del DOM después de la animación
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Confirmación de eliminación
confirmDeleteBtn.addEventListener('click', () => {
    if (!currentReportId) return;
    
    // Eliminar del arreglo de reportes
    reports = reports.filter(report => report.id !== currentReportId);
    
    // Eliminar de la tabla
    const row = document.querySelector(`.reports-table tbody tr[data-id="${currentReportId}"]`);
    if (row) {
        row.classList.add('fade-out');
        // Pequeña animación de desvanecimiento antes de eliminar
        setTimeout(() => {
            row.parentNode.removeChild(row);
        }, 300);
    }
    
    // Cerrar modal
    closeDeleteModal();
    
    // Mostrar notificación
    showNotification('Reporte eliminado con éxito');
});

// Filtrado de reportes
applyFiltersBtn.addEventListener('click', () => {
    filterReports();
});

// Función para filtrar reportes
function filterReports() {
    const dateFilter = filterDate.value;
    const statusFilter = filterStatus.value;
    const typeFilter = filterType.value;
    
    // Crear copia del arreglo original para no modificarlo
    let filteredReports = [...reports];
    
    // Filtrar por fecha
    if (dateFilter !== 'all') {
        const today = new Date();
        
        switch (dateFilter) {
            case 'today':
                const todayFormatted = formatDate(today);
                filteredReports = filteredReports.filter(r => r.date === todayFormatted);
                break;
                
            case 'week':
                // Obtener fecha de hace 7 días
                const weekAgo = new Date();
                weekAgo.setDate(today.getDate() - 7);
                filteredReports = filteredReports.filter(r => {
                    const reportDate = parseDate(r.date);
                    return reportDate >= weekAgo && reportDate <= today;
                });
                break;
                
            case 'month':
                // Obtener fecha de hace 30 días
                const monthAgo = new Date();
                monthAgo.setDate(today.getDate() - 30);
                filteredReports = filteredReports.filter(r => {
                    const reportDate = parseDate(r.date);
                    return reportDate >= monthAgo && reportDate <= today;
                });
                break;
                
            // Para el caso 'custom' se implementaría un datepicker
        }
    }
    
    // Filtrar por estado
    if (statusFilter !== 'all') {
        filteredReports = filteredReports.filter(r => r.status === statusFilter);
    }
    
    // Filtrar por tipo de servicio
    if (typeFilter !== 'all') {
        const typeMap = {
            'paint': 'Pintura completa',
            'partial': 'Pintado parcial',
            'repair': 'Reparación',
            'bodywork': 'Chapa y Pintura',
            'mechanical': 'Mecánico',
            'electrical': 'Eléctrico'
        };
        
        filteredReports = filteredReports.filter(r => r.type.includes(typeMap[typeFilter]));
    }
    
    // Actualizar tabla con los resultados filtrados
    updateReportsTable(filteredReports);
    
    // Mostrar notificación con la cantidad de resultados
    if (filteredReports.length === 0) {
        showNotification('No se encontraron reportes con los filtros seleccionados');
    } else {
        showNotification(`Se encontraron ${filteredReports.length} reportes`);
    }
}

// Función para actualizar la tabla con los reportes filtrados
function updateReportsTable(filteredReports) {
    const tbody = document.querySelector('.reports-table tbody');
    tbody.innerHTML = '';
    
    // Mapeo de estado a clase de badge
    const statusClassMap = {
        'completed': 'completed',
        'in-progress': 'in-progress',
        'pending': 'pending'
    };
    
    // Mapeo de estado a texto en español
    const statusTextMap = {
        'completed': 'Completado',
        'in-progress': 'En progreso',
        'pending': 'Pendiente'
    };
    
    filteredReports.forEach(report => {
        const row = document.createElement('tr');
        row.setAttribute('data-id', report.id);
        
        row.innerHTML = `
            <td>#${report.id}</td>
            <td>${report.client}</td>
            <td>${report.vehicle}</td>
            <td>${report.type}</td>
            <td>${report.date}</td>
            <td><span class="status-badge ${statusClassMap[report.status]}">${statusTextMap[report.status]}</span></td>
            <td class="action-buttons">
                <button class="btn-view" title="Ver reporte"><i class="fas fa-eye"></i></button>
                <button class="btn-edit" title="Editar reporte"><i class="fas fa-edit"></i></button>
                <button class="btn-delete" title="Eliminar reporte"><i class="fas fa-trash"></i></button>
            </td>
        `;
        
        tbody.appendChild(row);
        attachRowButtonListeners(row);
    });
}

// Funciones auxiliares para manejo de fechas
function parseDate(dateString) {
    // Convertir fecha en formato DD/MM/YYYY a objeto Date
    const parts = dateString.split('/');
    return new Date(parts[2], parts[1] - 1, parts[0]);
}

function formatDate(date) {
    // Convertir objeto Date a formato DD/MM/YYYY
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
}

// Inicializar botones de acción para filas existentes
document.addEventListener('DOMContentLoaded', () => {
    // Añadir listeners a filas existentes
    const rows = document.querySelectorAll('.reports-table tbody tr');
    rows.forEach(row => {
        attachRowButtonListeners(row);
    });
    
    // Event listener para botones de paginación
    const pageButtons = document.querySelectorAll('.pagination .btn-page');
    pageButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            // Quitar clase 'active' del botón actual
            document.querySelector('.pagination .btn-page.active')?.classList.remove('active');
            
            // Añadir clase 'active' al botón clickeado
            button.classList.add('active');
            
            // Si no es un botón de navegación (flechas), mostrar la página correspondiente
            if (!button.querySelector('i')) {
                const page = button.textContent;
                showNotification(`Mostrando página ${page}`);
                
                // Aquí se implementaría la lógica para cargar la página correspondiente
                // En un sistema real, esto haría una petición al servidor para obtener los datos de esa página
            }
        });
    });

    // Añadir funcionalidad de arrastrar y soltar para la carga de archivos
    const fileUpload = document.querySelector('.file-upload');
    const fileInput = document.getElementById('fileUpload');
    
    fileUpload.addEventListener('click', () => {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            updateFileUploadUI(fileInput.files);
        }
    });
    
    // Eventos de drag and drop
    fileUpload.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUpload.classList.add('drag-over');
    });
    
    fileUpload.addEventListener('dragleave', () => {
        fileUpload.classList.remove('drag-over');
    });
    
    fileUpload.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUpload.classList.remove('drag-over');
        
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            updateFileUploadUI(e.dataTransfer.files);
        }
    });

    // Añadir estilos adicionales para la interacción drag over
    const style = document.createElement('style');
    style.textContent = `
        .file-upload.drag-over {
            border-color: var(--primary-color);
            background-color: rgba(37, 99, 235, 0.05);
        }
        
        .file-preview {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
        }
        
        .file-item {
            display: flex;
            align-items: center;
            background-color: rgba(37, 99, 235, 0.1);
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
        }
        
        .file-item i {
            color: var(--primary-color);
            margin-right: 8px;
            font-size: 14px;
        }
        
        .file-item span {
            max-width: 150px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .fade-out {
            opacity: 0;
            transform: translateX(20px);
            transition: all 0.3s ease;
        }
    `;
    document.head.appendChild(style);
});

// Función para actualizar la UI después de seleccionar archivos
function updateFileUploadUI(files) {
    // Obtener o crear contenedor para la vista previa de archivos
    let filePreview = document.querySelector('.file-preview');
    
    if (!filePreview) {
        filePreview = document.createElement('div');
        filePreview.className = 'file-preview';
        document.querySelector('.file-upload').appendChild(filePreview);
    }
    
    // Limpiar vista previa existente
    filePreview.innerHTML = '';
    
    // Añadir cada archivo a la vista previa
    Array.from(files).forEach(file => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        // Determinar icono según tipo de archivo
        let icon = 'fa-file';
        
        if (file.type.startsWith('image/')) {
            icon = 'fa-file-image';
        } else if (file.type === 'application/pdf') {
            icon = 'fa-file-pdf';
        } else if (file.type.includes('word')) {
            icon = 'fa-file-word';
        } else if (file.type.includes('excel') || file.type.includes('sheet')) {
            icon = 'fa-file-excel';
        }
        
        fileItem.innerHTML = `
            <i class="fas ${icon}"></i>
            <span title="${file.name}">${file.name}</span>
        `;
        
        filePreview.appendChild(fileItem);
    });
    
    // Cambiar texto de la zona de carga
    const uploadText = document.querySelector('.file-upload p');
    if (files.length === 1) {
        uploadText.textContent = '1 archivo seleccionado';
    } else {
        uploadText.textContent = `${files.length} archivos seleccionados`;
    }
}

// Implementación de búsqueda en tiempo real
const searchInput = document.querySelector('.search-container input');

searchInput.addEventListener('input', () => {
    const searchTerm = searchInput.value.toLowerCase().trim();
    
    if (searchTerm === '') {
        // Si el término de búsqueda está vacío, restaurar la tabla original
        updateReportsTable(reports);
        return;
    }
    
    // Filtrar reportes que coincidan con el término de búsqueda
    const searchResults = reports.filter(report => {
        return (
            report.id.toLowerCase().includes(searchTerm) ||
            report.client.toLowerCase().includes(searchTerm) ||
            report.vehicle.toLowerCase().includes(searchTerm) ||
            report.type.toLowerCase().includes(searchTerm)
        );
    });
    
    // Actualizar tabla con resultados
    updateReportsTable(searchResults);
});

// Exportación de reportes
function exportToCSV() {
    // Obtener los reportes visibles actualmente en la tabla
    const visibleReports = [];
    const rows = document.querySelectorAll('.reports-table tbody tr');
    
    rows.forEach(row => {
        const reportId = row.getAttribute('data-id');
        const report = reports.find(r => r.id === reportId);
        if (report) {
            visibleReports.push(report);
        }
    });
    
    // Crear encabezados
    let csv = 'ID,Cliente,Vehículo,Tipo de Servicio,Fecha,Estado\n';
    
    // Añadir filas
    visibleReports.forEach(report => {
        const statusMap = {
            'completed': 'Completado',
            'in-progress': 'En Progreso',
            'pending': 'Pendiente'
        };
        
        csv += `${report.id},${report.client},${report.vehicle},${report.type},${report.date},${statusMap[report.status]}\n`;
    });
    
    // Crear blob y descargar
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    // Crear nombre de archivo con fecha actual
    const today = new Date();
    const filename = `reportes_${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}.csv`;
    
    if (navigator.msSaveBlob) { // Para IE
        navigator.msSaveBlob(blob, filename);
    } else {
        const url = URL.createObjectURL(blob);
        link.href = url;
        link.setAttribute('download', filename);
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }
    
    showNotification(`Exportación completada: ${visibleReports.length} reportes`);
}

// Añadir botón de exportación
document.addEventListener('DOMContentLoaded', () => {
    // Crear botón de exportación
    const exportBtn = document.createElement('button');
    exportBtn.className = 'btn-secondary';
    exportBtn.innerHTML = '<i class="fas fa-download"></i> Exportar CSV';
    exportBtn.addEventListener('click', exportToCSV);
    
    // Añadir a la sección de filtros
    const filterSection = document.querySelector('.filter-section');
    filterSection.appendChild(exportBtn);
    
    // Mejorar responsividad de la interfaz
    window.addEventListener('resize', adjustLayoutForScreenSize);
    adjustLayoutForScreenSize();
});

// Función para ajustar el layout según el tamaño de pantalla
function adjustLayoutForScreenSize() {
    const width = window.innerWidth;
    
    if (width < 768) {
        // Pantallas pequeñas - Mostrar/ocultar sidebar con botón
        if (!document.getElementById('sidebarToggle')) {
            const topBar = document.querySelector('.top-bar');
            const sidebarToggle = document.createElement('button');
            sidebarToggle.id = 'sidebarToggle';
            sidebarToggle.innerHTML = '<i class="fas fa-bars"></i>';
            sidebarToggle.className = 'sidebar-toggle';
            
            // Estilos para el botón
            sidebarToggle.style.background = 'none';
            sidebarToggle.style.border = 'none';
            sidebarToggle.style.fontSize = '22px';
            sidebarToggle.style.cursor = 'pointer';
            sidebarToggle.style.color = 'var(--text-color)';
            sidebarToggle.style.marginRight = '15px';
            
            // Añadir al principio del top-bar
            topBar.insertBefore(sidebarToggle, topBar.firstChild);
            
            // Evento para mostrar/ocultar sidebar
            sidebarToggle.addEventListener('click', () => {
                const sidebar = document.querySelector('.sidebar');
                sidebar.classList.toggle('expanded');
                
                // Si tiene la clase 'expanded', mostrar completo
                if (sidebar.classList.contains('expanded')) {
                    sidebar.style.width = '250px';
                    document.querySelector('.sidebar .logo h2').style.display = 'block';
                    
                    const navItems = document.querySelectorAll('.sidebar nav ul li a');
                    navItems.forEach(item => {
                        item.style.justifyContent = 'flex-start';
                        item.style.padding = '12px 20px';
                        const text = item.querySelector('span') || document.createElement('span');
                        if (!item.querySelector('span')) {
                            text.textContent = item.getAttribute('aria-label') || '';
                            item.appendChild(text);
                        }
                        item.querySelector('i').style.margin = '0 10px 0 0';
                    });
                } else {
                    sidebar.style.width = '70px';
                    document.querySelector('.sidebar .logo h2').style.display = 'none';
                    
                    const navItems = document.querySelectorAll('.sidebar nav ul li a');
                    navItems.forEach(item => {
                        item.style.justifyContent = 'center';
                        item.style.padding = '15px 0';
                        const text = item.querySelector('span');
                        if (text) text.style.display = 'none';
                        item.querySelector('i').style.margin = '0';
                    });
                }
            });
        }
    } else {
        // Pantallas grandes - Quitar botón de toggle si existe
        const sidebarToggle = document.getElementById('sidebarToggle');
        if (sidebarToggle) {
            sidebarToggle.remove();
        }
        
        // Restaurar sidebar
        const sidebar = document.querySelector('.sidebar');
        sidebar.style.width = '250px';
        document.querySelector('.sidebar .logo h2').style.display = 'block';
        
        const navItems = document.querySelectorAll('.sidebar nav ul li a');
        navItems.forEach(item => {
            item.style.justifyContent = 'flex-start';
            item.style.padding = '12px 20px';
            const text = item.querySelector('span') || document.createElement('span');
            if (!item.querySelector('span')) {
                text.textContent = item.getAttribute('aria-label') || '';
                item.appendChild(text);
            }
            text.style.display = 'inline';
            item.querySelector('i').style.margin = '0 10px 0 0';
        });
    }
}

// Capturar datos de gráficos para el dashboard (simulado)
function generateDashboardData() {
    // Esta función podría ser utilizada en una versión extendida
    // para generar datos de reporte para gráficos y estadísticas
    
    // Datos mensuales (últimos 6 meses)
    const monthlyData = [
        { month: 'Nov', count: 32 },
        { month: 'Dic', count: 28 },
        { month: 'Ene', count: 35 },
        { month: 'Feb', count: 42 },
        { month: 'Mar', count: 38 },
        { month: 'Abr', count: 47 }
    ];
    
    // Datos por tipo de servicio
    const serviceTypeData = [
        { type: 'Pintura', count: 87 },
        { type: 'Reparación', count: 63 },
        { type: 'Detailing', count: 45 },
        { type: 'Cambio color', count: 32 },
        { type: 'Otro', count: 20 }
    ];
    
    return {
        monthly: monthlyData,
        serviceTypes: serviceTypeData
    };
}
document.addEventListener("DOMContentLoaded", function () {
    const carrito = JSON.parse(localStorage.getItem("cart")) || [];
    const reserva = JSON.parse(localStorage.getItem("reserva")) || {};

    // Mostrar los datos de la reserva en la factura
    document.getElementById("nombreCliente").textContent = reserva.nombre || "No especificado";
    document.getElementById("apellidoCliente").textContent = reserva.apellido || "No especificado";
    document.getElementById("correoCliente").textContent = reserva.correo || "No especificado";
    document.getElementById("telefonoCliente").textContent = reserva.telefono || "No especificado";
    document.getElementById("comentarioCliente").textContent = reserva.comentario || "No especificado";
    document.getElementById("fechaHora").textContent = (reserva.fecha && reserva.hora) ? `${reserva.fecha} ${reserva.hora}` : "--";

    let subtotal = 0;
    const tablaServicios = document.getElementById("serviciosTabla");
    tablaServicios.innerHTML = ''; // Limpiar antes de agregar filas

    carrito.forEach((producto) => {
        let cantidad = producto.cantidad || 1;
        let precioUnitario = parseFloat(producto.price);
        let total = cantidad * precioUnitario;
        subtotal += total;

        let fila = `
            <tr>
                <td>${producto.name}</td>
                <td>${cantidad}</td>
                <td>${formatoCOP(precioUnitario)}</td>
                <td>${formatoCOP(total)}</td>
            </tr>
        `;
        tablaServicios.innerHTML += fila;
    });

    let descuento = 0;
    let total = subtotal - descuento;

    document.getElementById("subtotal").textContent = formatoCOP(subtotal);
    document.getElementById("descuento").textContent = formatoCOP(descuento);
    document.getElementById("total").textContent = formatoCOP(total);
    
    document.getElementById("fechaFactura").textContent = new Date().toLocaleDateString();
});

// Función para formatear precios en COP
function formatoCOP(valor) {
    return valor.toLocaleString('es-CO', { style: 'currency', currency: 'COP' });
}

function cargarReserva() {
    const reserva = JSON.parse(localStorage.getItem("reserva")) || {};

    document.getElementById("nombreCliente").textContent = reserva.nombre || "No especificado";
    document.getElementById("apellidoCliente").textContent = reserva.apellido || "No especificado";
    document.getElementById("correoCliente").textContent = reserva.correo || "No especificado";
    document.getElementById("telefonoCliente").textContent = reserva.telefono || "No especificado";
    document.getElementById("comentarioCliente").textContent = reserva.comentario || "No especificado";
    document.getElementById("fechaHora").textContent = reserva.fecha ? `${reserva.fecha} ${reserva.hora}` : "--";
}

document.addEventListener("DOMContentLoaded", function () {
    cargarReserva();
});

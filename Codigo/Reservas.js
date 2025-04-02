// Función para avanzar al siguiente paso (cliente)
function nextStep() {
    // Ocultar el primer formulario y mostrar el formulario de cliente
    document.getElementById('appointment-info').style.display = 'none';
    document.getElementById('client-info').style.display = 'block';

    // Rellenar el formulario de modificación con los valores actuales
    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('hora').value;

    // Mostrar la fecha y hora seleccionada
    document.getElementById('fecha-selected').textContent = fecha;
    document.getElementById('hora-selected').textContent = hora;
}

// Función para editar la fecha seleccionada
function editDate() {
    const fecha = document.getElementById('fecha-selected').textContent;
    // Comprobar si la fecha ya está disponible
    if (fecha !== '--') {
        document.getElementById('fecha').value = fecha;
    }
    // Mostrar el formulario de edición (si no está visible)
    document.getElementById('appointment-info').style.display = 'block';
}

// Función para editar la hora seleccionada
function editTime() {
    const hora = document.getElementById('hora-selected').textContent;
    // Comprobar si la hora ya está disponible
    if (hora !== '--') {
        document.getElementById('hora').value = hora;
    }
    // Mostrar el formulario de edición (si no está visible)
    document.getElementById('appointment-info').style.display = 'block';
}

// Función para editar el servicio seleccionado
function editService() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    if (cart.length === 0) {
        alert('No se ha seleccionado un servicio para editar.');
        return;
    }

    const serviceName = cart.map(item => item.name).join(", ");
    const newService = prompt('Editar Servicio:', serviceName);

    if (newService && newService !== serviceName) {
        // Actualizamos el servicio en el carrito
        cart.forEach(item => item.name = newService);  // Actualiza todos los productos del carrito si es necesario
        localStorage.setItem("cart", JSON.stringify(cart));
        updateCart(); // Llamar a la función que actualiza el carrito
        document.getElementById("servicio-selected").textContent = newService;
    }
}

// Función para actualizar el carrito en el modal
function updateCart() {
    const cartItemsContainer = document.getElementById('cartItems');
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('totalCart');
    const cart = JSON.parse(localStorage.getItem("cart")) || [];

    cartItemsContainer.innerHTML = ''; // Limpiar la lista de productos
    let subtotal = 0;

    cart.forEach((item, index) => {
        const productElement = document.createElement('div');
        productElement.classList.add('modal__item');
        productElement.innerHTML = `
            <div class="modal__thumb">
                <img src="${item.image}" alt="${item.name}">
            </div>
            <div class="modal__text-product">
                <p>${item.name}</p>
                <p><strong>$${parseFloat(item.price.replace(/\./g, '')).toLocaleString('es-CO')}</strong></p>
                <button class="remove-btn" data-index="${index}">Eliminar</button>
                <button class="edit-btn" data-index="${index}">Editar</button> <!-- Botón para editar -->
            </div>
        `;
        cartItemsContainer.appendChild(productElement);
        subtotal += parseFloat(item.price.replace(/\./g, ''));
    });

    // Actualizar subtotal y total
    subtotalElement.textContent = `$${subtotal.toLocaleString('es-CO')}`;
    totalElement.textContent = `Total: $${subtotal.toLocaleString('es-CO')}`;

    // Funcionalidad de eliminar
    const removeButtons = document.querySelectorAll('.remove-btn');
    removeButtons.forEach(btn => {
        btn.addEventListener('click', (event) => {
            const index = event.target.getAttribute('data-index');
            cart.splice(index, 1); // Eliminar producto del carrito
            localStorage.setItem("cart", JSON.stringify(cart)); // Guardar cambios
            updateCart(); // Actualizar el carrito
        });
    });

    // Funcionalidad de editar
    const editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(btn => {
        btn.addEventListener('click', (event) => {
            const index = event.target.getAttribute('data-index');
            editProduct(index); // Llamar a la función de edición
        });
    });
}


// Función para avanzar al siguiente paso (cliente)
function nextStep() {
    document.getElementById('appointment-info').style.display = 'none';
    document.getElementById('client-info').style.display = 'block';

    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('hora').value;

    document.getElementById('fecha-selected').textContent = fecha;
    document.getElementById('hora-selected').textContent = hora;
}

function guardarReserva() {
    const nombre = document.getElementById('nombre').value;
    const apellido = document.getElementById('apellido').value;
    const correo = document.getElementById('correo').value;
    const telefono = document.getElementById('telefono').value;
    const comentario = document.getElementById('comentario').value;
    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('hora').value;

    if (!nombre || !apellido || !correo || !telefono || !fecha || !hora) {
        alert("Por favor, complete todos los campos obligatorios.");
        return;
    }

    const reserva = { nombre, apellido, correo, telefono, comentario, fecha, hora };

    localStorage.setItem("reserva", JSON.stringify(reserva));
    console.log("Reserva guardada:", reserva);
}

document.getElementById("client-form").addEventListener("submit", function(event) {
    event.preventDefault();
    guardarReserva();
    window.location.href = "Factura.html"; // Redirige a la factura
});

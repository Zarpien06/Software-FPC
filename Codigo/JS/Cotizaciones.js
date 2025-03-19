const addToCart = document.querySelectorAll('[data-btn-action="add-btn-cart"]');
const closeModal = document.querySelector('.jsModalClose');
const modal = document.getElementById('jsModalCarrito');
const cartItemsContainer = document.getElementById('cartItems');
const subtotalElement = document.getElementById('subtotal');
const totalElement = document.getElementById('totalCart');

let cart = []; // Array para almacenar los productos del carrito

// Función para actualizar el carrito en el modal
function updateCart() {
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
            </div>
        `;
        cartItemsContainer.appendChild(productElement);
        subtotal += parseFloat(item.price.replace(/\./g, ''));
    });
    
    // Actualizar subtotal y total
    subtotalElement.textContent = `$${subtotal.toLocaleString('es-CO')}`;
    totalElement.textContent = `Total: $${subtotal.toLocaleString('es-CO')}`;

    // Agregar funcionalidad de eliminar
    const removeButtons = document.querySelectorAll('.remove-btn');
    removeButtons.forEach(btn => {
        btn.addEventListener('click', (event) => {
            const index = event.target.getAttribute('data-index');
            cart.splice(index, 1); // Eliminar producto del carrito
            updateCart(); // Actualizar el carrito
        });
    });
}


// Agregar productos al carrito
addToCart.forEach(btn => {
    btn.addEventListener('click', (event) => {
        const productElement = event.target.closest('.product-grid__item');
        const productName = productElement.getAttribute('data-name');
        const productPrice = productElement.getAttribute('data-price');
        const productImage = productElement.querySelector('img').src;
        
        const product = {
            name: productName,
            price: productPrice,
            image: productImage
        };

        // Agregar producto al carrito
        cart.push(product);

        // Abrir modal y actualizar
        modal.classList.add('active');
        updateCart();
    });
});

// Cerrar el modal
closeModal.addEventListener('click', () => {
    modal.classList.remove('active');
});

// Cerrar el modal haciendo clic fuera del contenido
window.onclick = (event) => {
    if (event.target === modal) {
        modal.classList.remove('active');
    }
};


    // Obtener el servicio seleccionado del localStorage
    const selectedService = localStorage.getItem("selectedService");
    if (selectedService) {
        document.getElementById('carrito').innerHTML = `Servicio seleccionado: ${selectedService}`;
    } else {
        document.getElementById('carrito').innerHTML = "No se ha seleccionado un servicio.";
    }



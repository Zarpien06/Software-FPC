// Ejemplo: Acción para el botón de cotizaciones
document.querySelector('.quote-button').addEventListener('click', () => {
    alert('Cotización iniciada. Por favor, completa los detalles.');
});

// Acción para las tarjetas (puedes expandirlo según tus necesidades)
document.querySelectorAll('.card-button').forEach(button => {
    button.addEventListener('click', () => {
        alert('Producto añadido al carrito.');
    });
});

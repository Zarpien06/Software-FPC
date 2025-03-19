let currentIndex = 0;

function moveSlide(direction) {
  const images = document.querySelector('.carousel-images');
  const totalImages = images.children.length;

  // Actualiza el índice de la imagen actual
  currentIndex = (currentIndex + direction + totalImages) % totalImages;

  // Cambia la posición del carrusel usando transform
  images.style.transform = `translateX(-${currentIndex * 100}%)`;
}
setInterval(() => moveSlide(1), 5000);

// Seleccionamos todas las preguntas
const faqQuestions = document.querySelectorAll('.faq-question');

// Agregamos un evento 'mouseover' para cada pregunta
faqQuestions.forEach(question => {
    question.addEventListener('mouseover', () => {
        const answer = question.nextElementSibling;
        if (answer && answer.classList.contains('faq-answer')) {
            answer.style.display = 'inline'; // Mostrar la respuesta
        }
    });

    question.addEventListener('mouseout', () => {
        const answer = question.nextElementSibling;
        if (answer && answer.classList.contains('faq-answer')) {
            answer.style.display = 'none'; // Ocultar la respuesta
        }
    });
});

// Seleccionar el botón y el menú
const menuToggle = document.getElementById('menu-toggle');
const navMenu = document.getElementById('nav-menu');

// Agregar evento al botón
menuToggle.addEventListener('click', function () {
    navMenu.classList.toggle('active'); // Alternar clase 'active'
});

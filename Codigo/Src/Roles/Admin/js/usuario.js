function irAIndex() {
    window.location.href = 'adminPrincipal.html'; 
}

function irAActualizar() {
    window.location.href = 'actualizar.html'; 
}

document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menu-toggle");
    const barraLateral = document.querySelector(".barra-lateral");
  
    // Evento para alternar la visibilidad de la barra lateral
    menuToggle.addEventListener("click", () => {
      barraLateral.classList.toggle("visible");
    });
  });

  const logoutLink = document.getElementById('logout-link');

    // Agregamos el evento 'click' al enlace
    logoutLink.addEventListener('click', function(e) {
      e.preventDefault(); // Prevenir acción por defecto del enlace

      // Mostrar alerta con SweetAlert
      Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Deseas cerrar la cuenta y salir de la aplicación?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, salir',
        cancelButtonText: 'No, cancelar'
      }).then((result) => {
        // Evaluar el resultado de la alerta
        if (result.isConfirmed) {
          // Si el usuario confirma, redirigir a index.html
          window.location.href = 'index.html';
        } else {
          // Si el usuario cancela, mostrar un mensaje de cancelación
          Swal.fire('Cancelado', 'No se cerró la sesión', 'info');
        }
      });
    });
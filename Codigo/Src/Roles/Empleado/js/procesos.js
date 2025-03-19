document.addEventListener("DOMContentLoaded", () => {
  // Referencias a los botones
  const btnModificar = document.querySelectorAll(".modificar-proceso");
  const btnAgregar = document.querySelector(".agregar-proceso");
  const btnEliminar = document.querySelector("#delate");

  // Referencias a los modales
  const modalModificar = document.querySelector(".modal-modificar");
  const modalNuevo = document.querySelector(".modal-nuevo");

  // Botones para cerrar modales
  const cerrarModales = document.querySelectorAll(".cerrar-modal");

  // Mostrar modal de modificar para cada botón de modificar
  btnModificar.forEach((btn) => {
      btn.addEventListener("click", () => {
          modalModificar.style.display = "block";
      });
  });

  // Mostrar modal de agregar
  btnAgregar.addEventListener("click", () => {
      modalNuevo.style.display = "block";
  });

  // Cerrar modales
  cerrarModales.forEach((btn) => {
      btn.addEventListener("click", () => {
          modalModificar.style.display = "none";
          modalNuevo.style.display = "none";
      });
  });

  // Cerrar modal al hacer clic fuera de ellos
  window.addEventListener("click", (e) => {
      if (e.target === modalModificar) modalModificar.style.display = "none";
      if (e.target === modalNuevo) modalNuevo.style.display = "none";
  });

  // Confirmación para eliminar un proceso
  btnEliminar.addEventListener("click", function (event) {
      event.preventDefault();
      Swal.fire({
          title: "¿Seguro que quiere eliminar este proceso?",
          showCancelButton: true,
          confirmButtonText: "Eliminar",
          cancelButtonText: "Cancelar",
      }).then((result) => {
          if (result.isConfirmed) {
              Swal.fire("Se eliminó exitosamente", "", "success");
          } else if (result.dismiss === Swal.DismissReason.cancel) {
              Swal.fire("Operación cancelada", "", "error");
          }
      });
  });

  // Confirmación para modificar un proceso
  document.querySelector(".guardar").addEventListener("click", function (event) {
      event.preventDefault();
      Swal.fire({
          title: "¿Está seguro de modificar este proceso?",
          showCancelButton: true,
          confirmButtonText: "Confirmar",
          cancelButtonText: "Cancelar",
      }).then((result) => {
          if (result.isConfirmed) {
              Swal.fire("Operación realizada", "", "success");
          } else if (result.dismiss === Swal.DismissReason.cancel) {
              Swal.fire("Operación cancelada", "", "error");
          }
      });
  });

  // Confirmación para agregar un proceso
  document.querySelector(".Gregar").addEventListener("click", function (event) {
      event.preventDefault();
      Swal.fire({
          title: "¿Está seguro de agregar este proceso?",
          showCancelButton: true,
          confirmButtonText: "Confirmar",
          cancelButtonText: "Cancelar",
      }).then((result) => {
          if (result.isConfirmed) {
              Swal.fire("Operación realizada", "", "success");
          } else if (result.dismiss === Swal.DismissReason.cancel) {
              Swal.fire("Operación cancelada", "", "error");
          }
      });
  });
});

// Función para redirigir al usuario
function irAIndex() {
  window.location.href = "empleado.html";
}

// Manejar el clic en "Administrar Usuario"  
document.getElementById('adminUsuarioToggle').addEventListener('click', function(event) {  
    event.preventDefault(); // Prevenir la redirección  
    const submenu = document.getElementById('userSubmenu');  
    // Alternar la visibilidad del submenú  
    submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';   
});  

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
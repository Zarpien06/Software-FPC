// Función para mostrar el formulario de edición
function mostrarFormularioEdicion() {
    const formulario = document.getElementById('formulario-edicion');
    formulario.classList.remove('oculto');
  }
  
  // Función para cerrar el formulario
  function cerrarFormulario() {
    const formulario = document.getElementById('formulario-edicion');
    formulario.classList.add('oculto');
  }
  
  // Función para guardar cambios con SweetAlert
  function guardarCambios() {    
    const nombre = document.getElementById('nombre').value;  
    const apellido = document.getElementById('apellido').value;
    const email = document.getElementById('email').value;  
    const number = document.getElementById('number').value;  
  
    // Usando SweetAlert con formato HTML
    Swal.fire({
      title: '¡Cambios guardados!',
      html: `
        <p>Nombre: ${nombre}</p>
        <p>Apellido: ${apellido}</p>
        <p>Email: ${email}</p>
        <p>Número: ${number}</p>`,
      icon: 'success',
      confirmButtonText: 'Aceptar'
    });
  
    cerrarFormulario();
  }
  
  
  // Función para manejar la acción de eliminar usuario
  function eliminarUsuario() {
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
  }
  
  
  // Función para redirigir al usuario
  function irAIndex() {
    window.location.href = "../adminPrincipal.html";
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
          window.location.href = '../index.html';
        } else {
          // Si el usuario cancela, mostrar un mensaje de cancelación
          Swal.fire('Cancelado', 'No se cerró la sesión', 'info');
        }
      });
    });
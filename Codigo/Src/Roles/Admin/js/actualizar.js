document.querySelector('.btn-volver').addEventListener('click', function(event) {
    event.preventDefault(); // Previene el comportamiento por defecto del botón
  
    Swal.fire({
      title: "Volver al inicio",
      icon: "info",
      html: `¿Seguro que quiere volver?`,
      showCloseButton: true,
      showCancelButton: true,
      focusConfirm: false,
      confirmButtonText: `<i class="fa fa-thumbs-up"></i> Seguro!`,
      confirmButtonAriaLabel: "Thumbs up, great!",
      cancelButtonText: `<i class="fa fa-thumbs-down"></i> No volver`,
      cancelButtonAriaLabel: "Thumbs down"
    }).then((result) => {
      if (result.isConfirmed) {
        // Acción para cuando el usuario confirma la alerta
        Swal.fire({
          title: "Redirigiendo...",
          text: "Ir a la página de usuario.",
          icon: "success"
        }).then(() => {
          window.location.href = "usuario.html"; // Redirige a la página
        });
      } else if (result.isDismissed) {
        // Acción si el usuario hace clic en cancelar o cierra la alerta
        Swal.fire({
          title: "Operación cancelada",
          text: "No se realizó ningún cambio.",
          icon: "info"
        });
      }
    });
  });
  

document.querySelector('.btn-actualizar').addEventListener('click', function(event) {
    event.preventDefault(); // Previene el comportamiento por defecto del botón
    
    Swal.fire({
        title: "Estas seguro de guardar estos cambios?",
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: "Guardar",
        denyButtonText: `No guardar`
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire("Guardado exitosamente", "", "success");
        } else if (result.isDenied) {
            Swal.fire("No se guardaron los cambios", "", "info");
        }
    });
});

document.querySelector('.btn-ingresar').addEventListener('click', function(event) {
    event.preventDefault(); // Previene el envío del formulario
    
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    if (email === '' || password === '') {
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Something went wrong!",
            footer: '<a href="#">Why do I have this issue?</a>'
        });
        return;
    }

    if (email === 'admin@maskot.com' && password === '12345') {
        Swal.fire({
            title: "Bienvenido",
            icon: "success",
            text: `
                Hola, admin.
                Has ingresado correctamente.
            `,
            confirmButtonText: `Ingresar`,
            confirmButtonAriaLabel: "Aceptar",
            cancelButtonText: `Cancelar`,
            cancelButtonAriaLabel: "Cancelar"
        }).then(() => {
            window.location.href = 'Administrador/DashboardAdministrador.html';
        });
        return;
    } else {
        Swal.fire({
            title: "Datos incorrectos",
            icon: "error",
            text: `Por favor, verifica tu email y contraseña`,
            showCloseButton: true,
            showCancelButton: false,
            focusConfirm: false,
            confirmButtonText: `Reintentar`,
            confirmButtonAriaLabel: "Aceptar",
            cancelButtonText: `Cancelar`,
            cancelButtonAriaLabel: "Cancelar"
        });
        return;
    }
});

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
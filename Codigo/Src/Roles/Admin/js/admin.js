
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

   /**
         * Función para abrir/cerrar los formularios
         * @param {string} modalId - ID del modal que se abrirá/cerrará
         */
   function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal.style.display === "block") {
        modal.style.display = "none";
    } else {
        modal.style.display = "block";
    }
}

document.addEventListener("DOMContentLoaded", () => {
  const actionButtons = document.querySelectorAll(".action-btn");
  const closeButtons = document.querySelectorAll(".close-btn");

  // Función para abrir un formulario modal
  const openForm = (targetId) => {
      const formModal = document.getElementById(targetId);
      if (formModal) {
          formModal.style.display = "block";
      }
  };

  // Función para cerrar un formulario modal
  const closeForm = (formModal) => {
      formModal.style.display = "none";
  };

  // Asignar eventos a los botones de acción
  actionButtons.forEach((button) => {
      button.addEventListener("click", () => {
          const targetId = button.getAttribute("data-target");
          openForm(targetId);
      });
  });

  // Asignar eventos a los botones de cerrar
  closeButtons.forEach((button) => {
      button.addEventListener("click", () => {
          const formModal = button.closest(".form-modal");
          closeForm(formModal);
      });
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

    // Mostrar vista previa de la imagen
imageInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
      imagePreview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  } else {
    imagePreview.style.display = 'none';
  }
});

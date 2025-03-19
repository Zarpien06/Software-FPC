// Referencias a los elementos
const toggleFormBtn = document.getElementById('toggle-form-btn');
const closeFormBtn = document.getElementById('close-form-btn');
const form = document.getElementById('agregar-auto-form');
const imageInput = document.getElementById('imagen-auto');
const imagePreview = document.getElementById('imagen-preview');

// Alternar visibilidad del formulario
toggleFormBtn.addEventListener('click', () => {
  if (form.style.display === 'block') {
    form.style.display = 'none'; // Ocultar
  } else {
    form.style.display = 'block'; // Mostrar
  }
});

// Cerrar formulario al presionar el botón de cerrar
closeFormBtn.addEventListener('click', () => {
  form.style.display = 'none';
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
          window.location.href = "adminPrincipal.html"; // Redirige a la página
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
            window.location.href = "adminPrincipal.html";
        } else if (result.isDenied) {
            Swal.fire("No se guardaron los cambios", "", "info");
        }
    });
});



  
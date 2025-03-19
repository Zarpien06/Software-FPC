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
  window.location.href = "adminPrincipal.html";
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

    document.addEventListener('DOMContentLoaded', function() {  
    const tablaPrincipal = document.getElementById('tabla-principal').getElementsByTagName('tbody')[0];  
    const tablaAdicional = document.getElementById('tabla-adicional').getElementsByTagName('tbody')[0];  

    function eliminarProceso(boton) {  
        const fila = boton.closest('tr');  
        const filas = tablaPrincipal.getElementsByTagName('tr');  

        // Mover la fila a la tabla adicional  
        if (filas.length > 2) {  
            tablaAdicional.appendChild(fila);  
        } else {  
            // Si no hay más filas en la tabla principal, eliminar la fila  
            fila.remove();  
        }  

        // Si no quedan filas en la tabla principal, ocultar la tabla  
        if (filas.length <= 1) {  
            document.getElementById('tabla-principal').style.display = 'none';  
        }  

        // Mostrar la tabla adicional si tiene elementos  
        if (tablaAdicional.childElementCount > 0) {  
            document.getElementById('tabla-adicional').style.display = 'block';  
        }  
    }  
});






document.getElementById('form-agregar').addEventListener('submit', function(event) {  
    event.preventDefault(); // Evita que el formulario se envíe de la manera tradicional  

    // Obtener los valores del formulario  
    const nombre = document.getElementById('agregar-nombre').value;  
    const valor = document.getElementById('agregar-valor').value;  
    const descripcion = document.getElementById('agregar-descripcion').value;  

    // Manejo de la imagen (opcional)  
    const imgUpload = document.getElementById('img-upload-agregar').files[0];  
    let imgSrc = '';  
    if (imgUpload) {  
        const reader = new FileReader();  
        reader.onload = function(e) {  
            imgSrc = e.target.result;  
            agregarFila(nombre, valor, descripcion, imgSrc);  
        }  
        reader.readAsDataURL(imgUpload);  
    } else {  
        agregarFila(nombre, valor, descripcion, imgSrc);  
    }  

    // Limpiar el formulario  
    this.reset();  
});  

function agregarFila(nombre, valor, descripcion, imgSrc) {  
    const tabla = document.getElementById('tabla-procesos').getElementsByTagName('tbody')[0];  
    const nuevaFila = tabla.insertRow();  

    // Crear celdas para la nueva fila  
    const celdaNombre = nuevaFila.insertCell(0);  
    const celdaValor = nuevaFila.insertCell(1);  
    const celdaDescripcion = nuevaFila.insertCell(2);  
    const celdaImagen = nuevaFila.insertCell(3);  

    // Asignar valores a las celdas  
    celdaNombre.textContent = nombre;  
    celdaValor.textContent = valor;  
    celdaDescripcion.textContent = descripcion;  

    // Crear y asignar la imagen  
    if (imgSrc) {  
        const img = document.createElement('img');  
        img.src = imgSrc;  
        img.alt = 'Imagen del proceso';  
        img.style.width = '50px'; // Ajusta el tamaño de la imagen si es necesario  
        celdaImagen.appendChild(img);  
    }  
}  

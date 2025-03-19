document.addEventListener("DOMContentLoaded", function () {
    // Recuperar datos de localStorage
    const credenciales = JSON.parse(localStorage.getItem("credenciales"));

    // Verificar si hay datos almacenados
    if (credenciales) {
        document.getElementById("telefono").textContent = credenciales.telefono;
        document.getElementById("correo").textContent = credenciales.correo;
      
    }
});
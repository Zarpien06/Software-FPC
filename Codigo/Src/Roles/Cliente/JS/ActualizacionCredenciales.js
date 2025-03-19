document.getElementById("updateForm").addEventListener("submit", function (event) {
    event.preventDefault();

    // Guardar datos en localStorage
    const credenciales = {
        telefono: document.getElementById("telefono").value,
        correo: document.getElementById("correo").value,
    };
    localStorage.setItem("credenciales", JSON.stringify(credenciales));

    // Redirigir a la página de credenciales
    window.location.href = "Credenciales.html";
});
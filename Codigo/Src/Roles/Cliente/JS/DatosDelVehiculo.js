document.addEventListener('DOMContentLoaded', () => {
    // Simulación de datos del vehículo cargados dinámicamente
    const vehicleData = {
        codigoUnico: "100",
        marca: "Toyota",
        modelo: "Corolla",
        matricula: "ABC123",
        fechaMatricula: "2021-05-20",
        nacionalidad: "Colombiana",
        bastidor: "JT1234567890",
        color: "Azul",
        potencia: "132",
        plazas: "5",
        combustible: "Diésel",
        sidecar: "No",
        remolque: "No",
        persona: "Juan Pérez",
        foto: "vehicle.jpg"
    };

    // Cargar datos en la página
    Object.entries(vehicleData).forEach(([key, value]) => {
        const element = document.getElementById(key);
        if (element) element.textContent = value;
    });
});

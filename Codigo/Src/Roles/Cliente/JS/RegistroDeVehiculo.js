function showVehicle(vehicleId) {
    const data = {
        1: {
            marca: "Toyota",
            modelo: "Corolla",
            color: "Azul",
            anio: 2020,
            motor: "1.8L",
            placa: "ABC123",
        },
        2: {
            marca: "Honda",
            modelo: "Civic",
            color: "Gris",
            anio: 2018,
            motor: "2.0L",
            placa: "DEF456",
        },
    };

    const vehicleInfo = data[vehicleId];
    document.getElementById("marca").innerText = vehicleInfo.marca;
    document.getElementById("modelo").innerText = vehicleInfo.modelo;
    document.getElementById("color").innerText = vehicleInfo.color;
    document.getElementById("anio").innerText = vehicleInfo.anio;
    document.getElementById("motor").innerText = vehicleInfo.motor;
    document.getElementById("placa").innerText = vehicleInfo.placa;
}

function goBack() {
    alert("Volviendo al menú principal.");
}

function accept() {
    alert("Datos confirmados.");
}

document.addEventListener('DOMContentLoaded', function() {
    const seleccionFechaHora = document.getElementById('seleccionFechaHora');
    const datosYCotizacion = document.getElementById('datosYCotizacion');
    const continuarSeleccion = document.getElementById('continuarSeleccion');
    const modificarHora = document.getElementById('modificarHora');
    const resDia = document.getElementById('resDia');
    const resHora = document.getElementById('resHora');
    const days = document.querySelectorAll('.days .list-item');
    const hours = document.querySelector('.hours .scrollable');
    const minutes = document.querySelector('.minutes .scrollable');
    const periods = document.querySelectorAll('.period .list-item');
    let selectedDay = '';
    let selectedHour = '';
    let selectedMinute = '';
    let selectedPeriod = '';

    // Generar horas y minutos dinámicamente
    for (let i = 0; i < 24; i++) {
        const hourItem = document.createElement('li');
        hourItem.classList.add('list-item');
        hourItem.textContent = i.toString().padStart(2, '0');
        hourItem.dataset.hour = i.toString().padStart(2, '0');
        hours.appendChild(hourItem);
    }

    for (let i = 0; i < 60; i++) {
        const minuteItem = document.createElement('li');
        minuteItem.classList.add('list-item');
        minuteItem.textContent = i.toString().padStart(2, '0');
        minuteItem.dataset.minute = i.toString().padStart(2, '0');
        minutes.appendChild(minuteItem);
    }

    // Seleccionar día
    days.forEach(day => {
        day.addEventListener('click', function() {
            selectedDay = this.dataset.dia;
            days.forEach(d => d.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    // Seleccionar hora
    hours.addEventListener('click', function(event) {
        if (event.target.classList.contains('list-item')) {
            selectedHour = event.target.dataset.hour;
            hours.querySelectorAll('.list-item').forEach(h => h.classList.remove('selected'));
            event.target.classList.add('selected');
        }
    });

    // Seleccionar minuto
    minutes.addEventListener('click', function(event) {
        if (event.target.classList.contains('list-item')) {
            selectedMinute = event.target.dataset.minute;
            minutes.querySelectorAll('.list-item').forEach(m => m.classList.remove('selected'));
            event.target.classList.add('selected');
        }
    });

    // Seleccionar periodo
    periods.forEach(period => {
        period.addEventListener('click', function() {
            selectedPeriod = this.dataset.period;
            periods.forEach(p => p.classList.remove('selected'));
            this.classList.add('selected');
        });
    });

    // Continuar a datos personales
    continuarSeleccion.addEventListener('click', function() {
        if (selectedDay && selectedHour && selectedMinute && selectedPeriod) {
            resDia.textContent = selectedDay;
            resHora.textContent = `${selectedHour}:${selectedMinute} ${selectedPeriod}`;
            seleccionFechaHora.classList.add('animate__fadeOut');
            setTimeout(() => {
                seleccionFechaHora.style.display = 'none';
                datosYCotizacion.style.display = 'block';
                datosYCotizacion.classList.add('animate__fadeIn');
            }, 500); // Tiempo de la animación
        } else {
            alert('Por favor, seleccione día, hora, minuto y turno.');
        }
    });

    // Modificar hora
    modificarHora.addEventListener('click', function() {
        datosYCotizacion.classList.add('animate__fadeOut');
        setTimeout(() => {
            datosYCotizacion.style.display = 'none';
            seleccionFechaHora.style.display = 'block';
            seleccionFechaHora.classList.add('animate__fadeIn');
        }, 500); // Tiempo de la animación
    });

    // Cancelar reserva
    document.getElementById('cancelarReserva').addEventListener('click', function() {
        datosYCotizacion.classList.add('animate__fadeOut');
        setTimeout(() => {
            datosYCotizacion.style.display = 'none';
            seleccionFechaHora.style.display = 'block';
            seleccionFechaHora.classList.add('animate__fadeIn');
        }, 500); // Tiempo de la animación
    });
});

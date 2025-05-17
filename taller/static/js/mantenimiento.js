// mantenimiento.js

document.addEventListener('DOMContentLoaded', function() {
    // Selecciona los elementos que deseas animar
    const forms = document.querySelectorAll('.formulario-item');

    // Añade una clase para iniciar la animación cuando la página se carga
    forms.forEach(form => {
        form.classList.add('fade-in');
    });
});
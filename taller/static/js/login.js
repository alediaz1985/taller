document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');

    form.addEventListener('submit', function (e) {
        // Resetear mensaje de error
        errorMessage.textContent = '';

        // Verificar si todos los campos están llenos
        const fields = form.querySelectorAll('input[type="text"], input[type="password"]');
        let valid = true;
        fields.forEach(field => {
            if (field.value.trim() === '') {
                valid = false;
            }
        });

        if (!valid) {
            e.preventDefault(); // Prevenir el envío del formulario
            errorMessage.textContent = 'Por favor, completa todos los campos.';
        }
    });
});

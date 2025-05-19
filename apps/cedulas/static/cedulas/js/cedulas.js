let cropperFrente, cropperDorso;

function iniciarCropper(inputId, previewId, cropDataId, botonId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    const cropDataInput = document.getElementById(cropDataId);
    const botonRecortar = document.querySelector(`[data-input="${inputId.replace('-input', '')}"]`);

    input.addEventListener('change', function () {
        const file = input.files[0];
        if (!file) return;

        const url = URL.createObjectURL(file);
        preview.src = url;
        preview.style.display = "block";

        preview.onload = function () {
            // Destruir cropper anterior si existe
            if (inputId === 'frente-input' && cropperFrente) cropperFrente.destroy();
            if (inputId === 'dorso-input' && cropperDorso) cropperDorso.destroy();

            const cropper = new Cropper(preview, {
                aspectRatio: 94 / 57,
                viewMode: 1,
                autoCropArea: 1,
                dragMode: 'move',             // 👉 permite mover la imagen
                movable: true,                // 👉 habilita arrastrar la imagen
                cropBoxMovable: false,        // ❌ desactiva mover el marco
                cropBoxResizable: false,      // ❌ desactiva redimensionar el marco
                center: true,
                background: false,
                responsive: true,
                ready() {
                    const data = cropper.getData(true);
                    cropDataInput.value = `${Math.round(data.x)},${Math.round(data.y)},${Math.round(data.width)},${Math.round(data.height)}`;
                },
                cropend() {
                    const data = cropper.getData(true);
                    cropDataInput.value = `${Math.round(data.x)},${Math.round(data.y)},${Math.round(data.width)},${Math.round(data.height)}`;
                }
            });

            if (inputId === 'frente-input') cropperFrente = cropper;
            if (inputId === 'dorso-input') cropperDorso = cropper;
        };
    });

    // Acción del botón "Recortar"
    botonRecortar.addEventListener('click', function () {
        let cropperActivo = inputId === 'frente-input' ? cropperFrente : cropperDorso;

        if (cropperActivo) {
            const canvas = cropperActivo.getCroppedCanvas({
                width: 880,
                height: 580
            });

            const recorteBase64 = canvas.toDataURL('image/png');

            // Crear nueva imagen ya recortada
            const nuevaImagen = new Image();
            nuevaImagen.src = recorteBase64;
            nuevaImagen.className = "imagen-preview";
            nuevaImagen.style.display = "block";

            // Obtener el contenedor padre y reemplazar la imagen antigua
            const previewOriginal = document.getElementById(previewId);
            const contenedor = previewOriginal.parentNode;
            contenedor.replaceChild(nuevaImagen, previewOriginal);

            // Eliminar cropper y limpiar referencias
            cropperActivo.destroy();
            if (inputId === 'frente-input') {
                cropperFrente = null;
            } else {
                cropperDorso = null;
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    iniciarCropper('frente-input', 'frente-preview', 'frente-crop', 'btn-crop-frente');
    iniciarCropper('dorso-input', 'dorso-preview', 'dorso-crop', 'btn-crop-dorso');
});

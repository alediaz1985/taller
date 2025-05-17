let cropperFrente, cropperDorso;

function iniciarCropper(inputId, previewId, cropDataId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    const cropDataInput = document.getElementById(cropDataId);

    input.addEventListener('change', function () {
        const file = input.files[0];
        if (!file) return;

        const url = URL.createObjectURL(file);
        preview.src = url;
        preview.style.display = "block";

        preview.onload = function () {
            if (inputId === 'frente-input' && cropperFrente) cropperFrente.destroy();
            if (inputId === 'dorso-input' && cropperDorso) cropperDorso.destroy();

            const cropper = new Cropper(preview, {
                aspectRatio: 90 / 56,
                viewMode: 1,
                autoCropArea: 1,
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
}

document.addEventListener('DOMContentLoaded', function () {
    iniciarCropper('frente-input', 'frente-preview', 'frente-crop');
    iniciarCropper('dorso-input', 'dorso-preview', 'dorso-crop');
});

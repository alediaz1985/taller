document.getElementById('folder-selector').addEventListener('change', function (e) {
    const files = e.target.files;
    if (files.length > 0) {
        const path = files[0].webkitRelativePath;
        const folderPath = path.split("/")[0];
        document.getElementById('ruta-input').value = folderPath;
    }
});
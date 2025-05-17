document.addEventListener("DOMContentLoaded", function() {
    const pdfCarousel = document.getElementById('pdfCarousel');
    
    if (pdfCarousel) {  // Asegúrate de que pdfCarousel no es null
        const items = Array.from(pdfCarousel.querySelectorAll('.carousel-item'));

        // Mezclar las diapositivas de manera aleatoria
        items.sort(() => Math.random() - 0.5);

        const carouselInner = pdfCarousel.querySelector('.carousel-inner');
        carouselInner.innerHTML = ''; // Limpiar el contenido existente

        items.forEach(item => carouselInner.appendChild(item));

        // Inicializar el carrusel con intervalo de 10 segundos
        $('#pdfCarousel').carousel({
            interval: 10000, // Cambiar cada 10 segundos
            wrap: true
        });
    } else {
        console.error('El elemento pdfCarousel no existe en el DOM');
    }
});
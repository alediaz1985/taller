document.addEventListener('DOMContentLoaded', () => {
    const text = document.querySelector('.logo-text');
    if (text) {
        text.style.visibility = 'hidden';
        text.classList.remove('logo-text');

        void text.offsetWidth; // reinicia la animación forzando reflow

        text.classList.add('logo-text');
    }
});

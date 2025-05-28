// ayuda.js personalizado sin Bootstrap

document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.accordion-button');

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const collapse = button.closest('.accordion-item').querySelector('.accordion-collapse');
      const isOpen = collapse.classList.contains('show');

      // Cerrar todos los paneles
      document.querySelectorAll('.accordion-collapse').forEach(panel => panel.classList.remove('show'));
      document.querySelectorAll('.accordion-button').forEach(btn => btn.classList.add('collapsed'));

      // Si estaba cerrado, abrir este
      if (!isOpen) {
        collapse.classList.add('show');
        button.classList.remove('collapsed');
        collapse.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});

// js/custom.js

// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
  // 1. Resaltar el link activo de la navegación
  const navLinks = document.querySelectorAll('.nav-horizontal a[href]');
  const currentPage = window.location.pathname.split('/').pop();
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
    }
  });

  // 2. Comportamiento interactivo del rating por estrellas
  document.querySelectorAll('.stars').forEach(starGroup => {
    const stars = Array.from(starGroup.querySelectorAll('label'));
    const radios = Array.from(starGroup.querySelectorAll('input[type="radio"]'));

    // Función para pintar estrellas hasta el índice indicado
    function paint(upTo) {
      stars.forEach((star, i) => {
        star.style.color = i <= upTo
          ? getComputedStyle(document.documentElement)
              .getPropertyValue('--star-color')
          : '#ccc';
      });
    }

    // Función para restaurar color según selección
    function reset() {
      const checkedIndex = radios.findIndex(r => r.checked);
      if (checkedIndex !== -1) {
        // Convertir índice de radio a índice de etiqueta
        const paintIndex = radios.length - 1 - checkedIndex;
        paint(paintIndex);
      } else {
        stars.forEach(s => s.style.color = '#ccc');
      }
    }

    stars.forEach((star, idx) => {
      // Hover: pintar estrellas de 0 hasta idx
      star.addEventListener('mouseenter', () => paint(idx));
      // Salir hover: restaurar selección
      star.addEventListener('mouseleave', reset);
      // Click: marcar el radio correspondiente
      star.addEventListener('click', () => {
        const radioIndex = radios.length - 1 - idx;
        radios[radioIndex].checked = true;
        reset();
      });
    });

    // Inicializar color según valor por defecto
    reset();
  });

  // 3. Confirmar antes de eliminar/actualizar
  document.querySelectorAll('.btn-outline-primary').forEach(btn => {
    btn.addEventListener('click', e => {
      const confirmed = confirm('¿Seguro que deseas continuar?');
      if (!confirmed) e.preventDefault();
    });
  });

  // 4. Indicador de carga en formularios al enviar
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML =
          `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...`;
      }
    });
  });
});

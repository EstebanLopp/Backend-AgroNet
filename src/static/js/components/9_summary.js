
document.addEventListener('DOMContentLoaded', function () {
  const summaryContainer = document.querySelector('.cart-page__summary-container');

  if (summaryContainer) {
    fetch('/src/templates/components/9_summary.html')      
    .then(response => response.text())
      .then(data => {
        summaryContainer.innerHTML = data;
      })
      .catch(error => console.error('Error cargando resumen-producto:', error));
  }
});

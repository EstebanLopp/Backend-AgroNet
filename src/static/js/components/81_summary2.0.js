document.addEventListener('DOMContentLoaded', function () {
  const contenedor = document.querySelector('.summary__product__container__general');

  if (contenedor) {
    fetch('/src/templates/components/81_summary2.0.html')      
    .then(response => response.text())
      .then(data => {
        contenedor.innerHTML = data;
      })
      .catch(error => console.error('Error cargando resumen-producto:', error));
  }
});

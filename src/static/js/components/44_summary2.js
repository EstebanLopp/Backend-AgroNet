document.addEventListener('DOMContentLoaded', function () {
  const contenedor = document.querySelector('.summary2__product__container');

  if (contenedor) {
    fetch('/src/templates/components/44_summary2.html')      
    .then(response => response.text())
      .then(data => {
        contenedor.innerHTML = data;
      })
      .catch(error => console.error('Error cargando resumen-producto:', error));
  }
});

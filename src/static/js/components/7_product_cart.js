document.addEventListener('DOMContentLoaded', () => {
  const contenedor = document.querySelector('.container__component');

  if (contenedor) {
    fetch('/src/templates/components/7_product_cart.html')
      .then(res => res.text())
      .then(html => {
        contenedor.innerHTML = html;
      })
      
      .catch(err => console.error('Error al cargar el producto:', err));
  }
});
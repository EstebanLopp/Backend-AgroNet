document.addEventListener('DOMContentLoaded', function () {
  const contenedor = document.querySelector('.order-customer-container');

  if (contenedor) {
    fetch('/src/templates/components/50_order_detail_customer.html')
      .then(response => response.text())
      .then(data => {
        contenedor.innerHTML = data;

        // Selección de elementos del modal
        const openBtn = document.querySelector('.order-detail__open-invoice');
        const modal = document.querySelector('.order-detail__invoice-modal');
        const closeBtn = document.querySelector('.order-detail__invoice-close');
        const overlay = document.querySelector('.order-detail__invoice-overlay');

        if (openBtn && modal && closeBtn && overlay) {

          openBtn.addEventListener("click", () => {
            modal.classList.add("active");
          });

          closeBtn.addEventListener("click", () => {
            modal.classList.remove("active");
          });

          overlay.addEventListener("click", () => {
            modal.classList.remove("active");
          });
        }
      })
      .catch(error => console.error('Error cargando componente:', error));
  }
});

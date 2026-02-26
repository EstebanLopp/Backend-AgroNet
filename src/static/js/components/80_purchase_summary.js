
document.addEventListener("DOMContentLoaded", () => {

  const cartData = [
    { vendor: "AgroJuan", phone: "3001234567", payment: "Nequi: 3001234567", products: [ { name: "Tomates", qty: 2, price: 8000 }, { name: "Papa criolla", qty: 1, price: 5000 } ] },
    { vendor: "CampoDulce", phone: "3217654321", payment: "Bancolombia: 12345", products: [ { name: "Miel pura", qty: 1, price: 18000 } ] },
    { vendor: "FruverCampo", phone: "3123647824", payment: "Daviplata: 12345", products: [ { name: "Tomate de arbol", qty: 3, price: 15000 } ] }
  ];

  const container = document.querySelector(".checkout-summary-customer");

  if (container) {
    fetch("/src/templates/components/80_purchase_summary.html")
      .then(res => res.text())
      .then(html => {
        container.innerHTML = html;
        renderSummary(cartData);
        initPopups();
      });
  }

  function renderSummary(data) {
    const vendorsContainer = document.querySelector(".checkout-summary__vendors--js");
    const confirmBtn = document.querySelector(".checkout-summary__confirm-btn--js");

    if (!vendorsContainer || !confirmBtn) return;

    data.forEach(v => {
      const vendorCard = document.createElement("div");
      vendorCard.className = "checkout-summary__vendor-card";

      vendorCard.innerHTML = `
        <h3 class="checkout-summary__vendor-name">${v.vendor}</h3>
        <ul class="checkout-summary__product-list">
          ${v.products.map(p => `
            <li class="checkout-summary__product-item">
              ${p.qty}x ${p.name} - $${p.price}
            </li>
          `).join("")}
        </ul>
        <p class="checkout-summary__contact-info"><strong>WhatsApp:</strong> ${v.phone}</p>
        <p class="checkout-summary__contact-info"><strong>Pago:</strong> ${v.payment}</p>
      `;

      vendorsContainer.appendChild(vendorCard);
    });

    confirmBtn.addEventListener("click", () => {
      document.querySelector(".checkout-summary__popup--confirm").classList.add("checkout-summary__popup--show");
    });
  }

  function initPopups() {
    const confirmPopup = document.querySelector(".checkout-summary__popup--confirm");
    const successPopup = document.querySelector(".checkout-summary__popup--success");

    if (!confirmPopup || !successPopup) return;

    const closeConfirm = confirmPopup.querySelector(".checkout-summary__popup-close");
    const cancelBtn = confirmPopup.querySelector(".checkout-summary__btn--cancel");
    const acceptBtn = confirmPopup.querySelector(".checkout-summary__btn--accept");
    const confirmContent = confirmPopup.querySelector(".checkout-summary__popup-content");
    const successContent = successPopup.querySelector(".checkout-summary__popup-content");
    const closeSuccess = successPopup.querySelector(".checkout-summary__popup-close");

    [closeConfirm, cancelBtn].forEach(btn => {
      btn.addEventListener("click", () => {
        confirmPopup.classList.remove("checkout-summary__popup--show");
      });
    });

    confirmPopup.addEventListener("click", e => {
      if (e.target === confirmPopup) confirmPopup.classList.remove("checkout-summary__popup--show");
    });

    confirmContent.addEventListener("click", e => e.stopPropagation());

    acceptBtn.addEventListener("click", () => {
      confirmPopup.classList.remove("checkout-summary__popup--show");
      successPopup.classList.add("checkout-summary__popup--show");
    });

    closeSuccess.addEventListener("click", () => {
      successPopup.classList.remove("checkout-summary__popup--show");
      window.location.href = "/src/templates/seller-pages/historial_orders.html";
    });

    successPopup.addEventListener("click", e => {
      if (e.target === successPopup) {
        successPopup.classList.remove("checkout-summary__popup--show");
        window.location.href = "/src/templates/seller-pages/historial_orders.html";
      }
    });

    successContent.addEventListener("click", e => e.stopPropagation());
  }

});



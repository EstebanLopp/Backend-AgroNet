document.addEventListener("DOMContentLoaded", function () {
  const openButton = document.querySelector(".order-detail__open-invoice");
  const modal = document.querySelector(".order-detail__invoice-modal");
  const closeButton = document.querySelector(".order-detail__invoice-close");

  if (!openButton || !modal) return;

  function openModal() {
    modal.classList.add("is-active");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    modal.classList.remove("is-active");
    document.body.style.overflow = "";
  }

  openButton.addEventListener("click", openModal);

  if (closeButton) {
    closeButton.addEventListener("click", closeModal);
  }

  modal.addEventListener("click", function (event) {
    if (event.target === modal) {
      closeModal();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && modal.classList.contains("is-active")) {
      closeModal();
    }
  });
});
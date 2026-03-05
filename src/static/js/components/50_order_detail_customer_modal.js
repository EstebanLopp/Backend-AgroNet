document.addEventListener("DOMContentLoaded", () => {
  const openBtn = document.querySelector(".order-detail__open-invoice");
  const modal = document.querySelector(".order-detail__invoice-modal");
  const closeBtn = document.querySelector(".order-detail__invoice-close");
  const overlay = document.querySelector(".order-detail__invoice-overlay");

  if (!openBtn || !modal) return;

  function openModal() {
    modal.classList.add("active");
  }

  function closeModal() {
    modal.classList.remove("active");
  }

  openBtn.addEventListener("click", openModal);
  closeBtn?.addEventListener("click", closeModal);
  overlay?.addEventListener("click", closeModal);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
  });
});
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modal-contact");
  if (!modal) return;

  const closeBtn = modal.querySelector(".close1");
  const okIcon = modal.querySelector(".ok");

  function cerrarModal() {
    modal.classList.remove("active");
  }

  closeBtn?.addEventListener("click", cerrarModal);
  okIcon?.addEventListener("click", cerrarModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) cerrarModal();
  });
});
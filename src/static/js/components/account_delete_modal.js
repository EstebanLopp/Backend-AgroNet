document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("delete-account-form");
  const modal = document.getElementById("account-delete-modal");
  const openBtn = document.getElementById("open-delete-account-modal");
  const closeBtn = document.getElementById("close-delete-account-modal");
  const cancelBtn = document.getElementById("cancel-delete-account-modal");
  const confirmBtn = document.getElementById("confirm-delete-account-modal");
  const overlay = modal?.querySelector(".account-delete-modal__overlay");

  if (!form || !modal || !openBtn || !confirmBtn) return;

  function openModal() {
    modal.classList.add("is-active");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    modal.classList.remove("is-active");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  openBtn.addEventListener("click", openModal);
  closeBtn?.addEventListener("click", closeModal);
  cancelBtn?.addEventListener("click", closeModal);
  overlay?.addEventListener("click", closeModal);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && modal.classList.contains("is-active")) {
      closeModal();
    }
  });

  confirmBtn.addEventListener("click", () => {
    form.submit();
  });
});
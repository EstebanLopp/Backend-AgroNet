document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".store-profile-container");

  if (container) {
    fetch("/src/templates/components/37_profile_store.html")
      .then(response => response.text())
      .then(data => {
        container.innerHTML = data;

        
        requestAnimationFrame(() => {
          initStoreProfileModals(); 
        });
      })
      .catch(error => console.error("Error loading store profile:", error));
  }
});




function initStoreProfileModals() {
  const btnDisable = document.querySelector(".store-profile__button--disable-store");
  const modalConfirm = document.querySelector(".store-profile__modal--confirm");
  const modalSuccess = document.querySelector(".store-profile__modal--success");

  if (!btnDisable || !modalConfirm || !modalSuccess) return;

  const btnCancel = modalConfirm.querySelector(".store-profile__modal-button--cancel");
  const btnAccept = modalConfirm.querySelector(".store-profile__modal-button--accept");
  const btnCloseSuccess = modalSuccess.querySelector(".store-profile__modal-close--success");
  const btnCloseConfirm = modalConfirm.querySelector(".store-profile__modal-close");

  
  btnDisable.addEventListener("click", () => {
    modalConfirm.classList.add("store-profile__modal--active");
  });

  
  btnCloseConfirm.addEventListener("click", () => {
    modalConfirm.classList.remove("store-profile__modal--active");
  });

  
  btnCancel.addEventListener("click", () => {
    modalConfirm.classList.remove("store-profile__modal--active");
  });

  
  btnAccept.addEventListener("click", () => {
    modalConfirm.classList.remove("store-profile__modal--active");
    modalSuccess.classList.add("store-profile__modal--active");
  });

  
  btnCloseSuccess.addEventListener("click", () => {
    modalSuccess.classList.remove("store-profile__modal--active");
    window.location.href = "/src/static/customer-pages/start_sales.html"; 
  });

  
  modalConfirm.addEventListener("click", (e) => {
    if (e.target === modalConfirm) {
      modalConfirm.classList.remove("store-profile__modal--active");
    }
  });

  
  modalSuccess.addEventListener("click", (e) => {
    if (e.target === modalSuccess) {
      modalSuccess.classList.remove("store-profile__modal--active");
    }
  });

  
  modalConfirm.querySelector(".store-profile__modal-content")
    .addEventListener("click", (e) => e.stopPropagation());

  modalSuccess.querySelector(".store-profile__modal-content")
    .addEventListener("click", (e) => e.stopPropagation());
}

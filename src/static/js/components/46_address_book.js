document.addEventListener("DOMContentLoaded", async () => {
  const containerPage = document.querySelector(".myaddressbook");

  if (containerPage) {
    try {
      const response = await fetch("/src/templates/components/46_address_book.html");
      const html = await response.text();
      containerPage.insertAdjacentHTML("beforeend", html);

      await loadContacts();
    } catch (err) {
      console.error("Error cargando HTML del componente:", err);
    }
  }
});

async function loadContacts() {
  const container = document.querySelector(".address-book__list");
  const template = document.querySelector(".address-book__template");
  const popup = document.querySelector(".address-book__popup");
  const modal = document.querySelector(".address-book__modal");

  
  const btnCancel = popup?.querySelector(".address-book__popup-btn--cancel");
  const btnAccept = popup?.querySelector(".address-book__popup-btn--accept");
  const modalClose = modal?.querySelector(".address-book__modal-close");

  if (!container || !template || !popup || !modal) {
    console.error("Faltan elementos del DOM para address-book (revisa el HTML insertado).");
    return;
  }

  let cardToDelete = null; 

  
  try {
    const res = await fetch("/src/static/data/address_book.json");
    const data = await res.json();

    container.innerHTML = "";

    data.forEach((item) => {
      const clone = template.content.cloneNode(true);

      clone.querySelector(".address-book__name").textContent = item.usuario ?? "";
      clone.querySelector(".address-book__label--username").textContent = item.nombre ?? "";
      clone.querySelector(".address-book__label--mail").textContent = item.correo ?? "";
      clone.querySelector(".address-book__label--phone").textContent = item.telefono ?? "";

      container.appendChild(clone);
    });
  } catch (err) {
    console.error("Error cargando JSON de contactos:", err);
    return;
  }

  
  document.addEventListener("click", (e) => {
    const target = e.target;

    
    if (target.classList.contains("address-book__options-btn")) {
      e.stopPropagation();
      
      document.querySelectorAll(".address-book__options-menu").forEach(m => {
        if (m !== target.nextElementSibling) m.style.display = "none";
      });

      const menu = target.nextElementSibling;
      if (menu) {
        menu.style.display = (menu.style.display === "block") ? "none" : "block";
      }
      return;
    }

    
    if (target.classList.contains("address-book__option--profile")) {
      const card = target.closest(".address-book__card");
      const usuario = card?.querySelector(".address-book__name")?.textContent ?? "";
      if (usuario) {
        window.location.href =
          `/src/templates/seller-pages/customer-profile.html?usuario=${encodeURIComponent(usuario)}`;
      }
      
      document.querySelectorAll(".address-book__options-menu").forEach(m => m.style.display = "none");
      return;
    }

    
    if (target.classList.contains("address-book__option--delete")) {
      const card = target.closest(".address-book__card");
      if (card) {
        cardToDelete = card;
        popup.style.display = "flex";
      }
      
      document.querySelectorAll(".address-book__options-menu").forEach(m => m.style.display = "none");
      return;
    }

    
    if (!target.closest(".address-book__options") ) {
      document.querySelectorAll(".address-book__options-menu").forEach(m => m.style.display = "none");
    }
  });

  
  btnCancel?.addEventListener("click", () => {
    popup.style.display = "none";
    cardToDelete = null;
  });

  
  btnAccept?.addEventListener("click", () => {
    if (cardToDelete && cardToDelete.remove) {
      cardToDelete.remove();
    } else {
      console.warn("No hay tarjeta válida para eliminar.");
    }
    cardToDelete = null;
    popup.style.display = "none";
    
    modal.style.display = "flex";
  });

  
  modalClose?.addEventListener("click", () => {
    modal.style.display = "none";
  });

  
  popup.addEventListener("click", (e) => {
    if (e.target === popup) {
      popup.style.display = "none";
      cardToDelete = null;
    }
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
  });
}

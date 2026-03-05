document.addEventListener("DOMContentLoaded", () => {
  
  const container = document.createElement("div");
  container.id = "logout_popup_container";
  document.body.appendChild(container);

  
  fetch("/src/templates/components/39_logout_popup.html")
    .then(response => response.text())
    .then(html => {
      container.innerHTML = html;
      inicializarLogoutPopup();
    })
    .catch(err => console.error("Error al cargar logout_popup:", err));
});

function inicializarLogoutPopup() {
  const popup = document.getElementById("logout_popup");
  const modal = document.getElementById("logout_success_modal");

  document.addEventListener("click", (e) => {
    
    if (e.target.closest("#logoutBtn")) {
      e.preventDefault();
      popup.style.display = "flex";
    }

    
    if (e.target.closest("#logout_cancel")) {
      popup.style.display = "none";
    }

    
    if (e.target.closest("#logout_accept")) {
      popup.style.display = "none";
      mostrarModalCierre();
    }

    
    if (e.target === popup) {
      popup.style.display = "none";
    }
  });
}


function mostrarModalCierre() {
  const modal = document.getElementById("logout_success_modal");

  if (!modal) {
    console.error("No se encontró el modal logout_success_modal");
    return;
  }

  modal.style.display = "flex";

  
  setTimeout(() => {
    const closeModalBtn = modal.querySelector(".close");
    const modalContent = modal.querySelector(".modal-content");

    const redirect = () => {
      window.location.href = "/src/templates/pages-general/index.html";
    };

    
    if (closeModalBtn) {
      closeModalBtn.addEventListener("click", redirect);
    }

    
    modal.addEventListener("click", (e) => {
      if (e.target === modal) redirect();
    });

    
    if (modalContent) {
      modalContent.addEventListener("click", (e) => {
        e.stopPropagation(); 
        redirect();
      });
    }
  }, 50); 
}

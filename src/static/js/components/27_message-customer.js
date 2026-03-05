async function cargarMensaje() {
  const contenedor = document.querySelector(".contacttwo-container");

  try {
    
    const resForm = await fetch("/src/templates/components/19_message.html");
    const htmlForm = await resForm.text();
    const div = document.createElement("div");
    div.innerHTML = htmlForm;
    contenedor.appendChild(div);

    
    const resModal = await fetch("/src/templates/components/52_popup_contact.html");
    const htmlModal = await resModal.text();
    document.body.insertAdjacentHTML("beforeend", htmlModal);

    
    inicializarModal();

  } catch (error) {
    console.error("Error al cargar los componentes:", error);
  }
}

function inicializarModal() {
  const form = document.getElementById("mensaje-form__form");
  const modal = document.getElementById("modal-contact");

  if (!form || !modal) {
    console.error("No se encontró el formulario o el modal en el DOM");
    return;
  }

  const closeBtn = modal.querySelector(".close1");
  const okIcon = modal.querySelector(".ok");

  
  const redireccion = "/src/templates/pages-general/contact-customer.html";

  
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    modal.style.display = "flex";
  });

  
  function cerrarYRedirigir() {
    modal.style.display = "none";
    window.location.href = redireccion;
  }

  
  closeBtn.addEventListener("click", cerrarYRedirigir);
  okIcon.addEventListener("click", cerrarYRedirigir);

  
  window.addEventListener("click", (e) => {
    if (modal.style.display === "flex") {
      cerrarYRedirigir();
    }
  });
}

cargarMensaje();

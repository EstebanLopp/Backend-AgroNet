async function cargarMensaje() {
  const contenedor = document.querySelector(".contacttwo-container");

  try {
    // Cargar el formulario
    const resForm = await fetch("/src/templates/components/19_message.html");
    const htmlForm = await resForm.text();
    const div = document.createElement("div");
    div.innerHTML = htmlForm;
    contenedor.appendChild(div);

    // Cargar el modal (al final del body)
    const resModal = await fetch("/src/templates/components/52_popup_contact.html");
    const htmlModal = await resModal.text();
    document.body.insertAdjacentHTML("beforeend", htmlModal);

    // Inicializar funcionalidad del modal
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

  // Página a la que redirigirá al cerrar el modal
  const redireccion = "/src/templates/pages-general/contact-customer.html";

  // Mostrar modal al enviar
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    modal.style.display = "flex";
  });

  // Cerrar o redirigir al hacer clic en cualquier parte
  function cerrarYRedirigir() {
    modal.style.display = "none";
    window.location.href = redireccion;
  }

  // Clic en la X o en el ícono ✔
  closeBtn.addEventListener("click", cerrarYRedirigir);
  okIcon.addEventListener("click", cerrarYRedirigir);

  // Clic fuera del contenido del modal o en cualquier parte
  window.addEventListener("click", (e) => {
    if (modal.style.display === "flex") {
      cerrarYRedirigir();
    }
  });
}

cargarMensaje();

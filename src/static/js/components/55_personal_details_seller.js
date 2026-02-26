async function cargarMensaje() {
  const contenedor = document.querySelector(".contact-seller-container");

  const res = await fetch("/src/templates/components/55_personal_details_seller.html");   // tu archivo con el formulario de mensaje
  const html = await res.text();

  const div = document.createElement("div");
  div.innerHTML = html;
  contenedor.appendChild(div);
}

cargarMensaje();

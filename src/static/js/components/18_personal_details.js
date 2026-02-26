async function cargarDatos() {
  const contenedor = document.querySelector(".contact-container");

  const res = await fetch("/templates/components/18_personal_details.html");   
  const html = await res.text();

  const div = document.createElement("div");
  div.innerHTML = html;
  contenedor.appendChild(div);
}

cargarDatos();

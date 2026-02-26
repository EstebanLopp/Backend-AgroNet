async function cargarMensaje() {
  const contenedor = document.querySelector(".contacttwo-container");

  const res = await fetch("/src/templates/components/28_personaldetailstwo.html");   // tu archivo con el formulario de mensaje
  const html = await res.text();

  const div = document.createElement("div");
  div.innerHTML = html;
  contenedor.appendChild(div);
}

cargarMensaje();

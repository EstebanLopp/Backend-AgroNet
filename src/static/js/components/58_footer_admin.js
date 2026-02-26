document.addEventListener("DOMContentLoaded", () => {
  const container = document.createElement("div");
  container.classList.add("footer-admin-container");
  document.body.appendChild(container);

  fetch("/src/templates/components/58_footer_admin.html")
    .then(response => response.text())
    .then(html => {
      container.innerHTML = html;
    })
    .catch(error => console.error("Error al cargar el footer del admin:", error));
});

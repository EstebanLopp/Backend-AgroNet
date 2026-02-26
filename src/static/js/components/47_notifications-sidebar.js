document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".account-content"); 
  // Ajusta el selector según tu layout principal
  if (container) {
    fetch("/src/templates/components/47_notifications-sidebar.html")
      .then(response => response.text())
      .then(data => {
        container.innerHTML = data;
      })
      .catch(error => console.error("Error al cargar las notificaciones:", error));
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".admin-view");
  if (!container) {
    console.error("No existe un contenedor .admin-view en este documento.");
    return;
  }

  fetch("/src/templates/components/59_admin_dashboard.html")
    .then(response => {
      if (!response.ok) throw new Error("Error al cargar el dashboard");
      return response.text();
    })
    .then(html => {
      container.innerHTML = html;

      
      const canvas = container.querySelector(".admin-dashboard__chart-canvas");
      if (!canvas) {
        console.error("No se encontró el canvas .admin-dashboard__chart-canvas");
        return;
      }

      new Chart(canvas, {
        type: "bar",
        data: {
          labels: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"],
          datasets: [
            {
              label: "Registros en la pagina",
              data: [120, 190, 300, 250, 280, 350],
              backgroundColor: "rgba(75, 192, 192, 0.6)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
              borderRadius: 8
            }
          ]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                color: "#333",
                font: { size: 13, weight: "500" }
              },
              grid: { color: "#eee" }
            },
            x: {
              ticks: { color: "#333" },
              grid: { color: "#fafafa" }
            }
          },
          plugins: {
            legend: { display: true, labels: { color: "#444" } },
            tooltip: { backgroundColor: "#fff", titleColor: "#000", bodyColor: "#333" }
          }
        }
      });
    })
    .catch(error => console.error("Error cargando el dashboard:", error));
});

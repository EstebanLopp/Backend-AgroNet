document.addEventListener("DOMContentLoaded", function() {
    const heroElement = document.querySelector(".navbar-container");

    if(heroElement) {
        fetch("/src/templates/components/5_navbar_seller.html")
        .then(response => response.text())
        .then(data => {
            heroElement.innerHTML = data; 
        })

    .catch(error => console.log("Error al cargar el hero", error));
    }
});
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("recommendationForm");
    const loading = document.getElementById("loading");
    const resultsContainer = document.getElementById("resultsContainer");
    const recommendationsList = document.getElementById("recommendationsList");
    const formSection = document.getElementById("formSection");

    // Ocultar secciones al inicio
    loading.style.display = "none";
    resultsContainer.style.display = "none";

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Mostrar loading
        formSection.style.display = "none";
        loading.style.display = "block";
        resultsContainer.style.display = "none";

        try {
            // Recuperar usuario actual desde localStorage (guardado en login)
            const user = JSON.parse(localStorage.getItem("user") || "{}");
            const username = user.userName || user.email || "estudiante";

            // Ejemplo: cursos aprobados guardados en localStorage o puedes pedirlos al backend
            const cursosAprobados = user.cursos_aprobados || ["MatematicasI", "ProgramacionBasica"];

            // Body para el API
            const body = {
                username: username,
                cursos_aprobados: cursosAprobados
            };

            const response = await fetch("http://localhost:2000/cursos/recomendados", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(body)
            });

            if (!response.ok) {
                throw new Error("Error al consultar la API");
            }

            const data = await response.json();

            // Mostrar resultados
            recommendationsList.innerHTML = "";

            if (data.cursos_disponibles && data.cursos_disponibles.length > 0) {
                const cursosHTML = `
                    <h3>Cursos disponibles:</h3>
                    <ul>
                        ${data.cursos_disponibles.map(c => `<li>${c}</li>`).join("")}
                    </ul>
                `;
                recommendationsList.innerHTML += cursosHTML;
            }

            if (data.recomendacion) {
                const recHTML = `
                    <h3>Recomendación del Asistente:</h3>
                    <p>${data.recomendacion}</p>
                `;
                recommendationsList.innerHTML += recHTML;
            }

            // Mostrar resultados y ocultar loading
            loading.style.display = "none";
            resultsContainer.style.display = "block";

        } catch (error) {
            console.error(error);
            recommendationsList.innerHTML = "<p>Error al obtener recomendaciones.</p>";
            loading.style.display = "none";
            resultsContainer.style.display = "block";
        }
    });
});

// Función para nueva consulta
function nuevaConsulta() {
    document.getElementById("formSection").style.display = "block";
    document.getElementById("loading").style.display = "none";
    document.getElementById("resultsContainer").style.display = "none"
}
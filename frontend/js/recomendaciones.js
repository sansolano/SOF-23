document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("recommendationForm");
    const loading = document.getElementById("loading");
    const resultsContainer = document.getElementById("resultsContainer");
    const recommendationsList = document.getElementById("recommendationsList");
    const formSection = document.getElementById("formSection");

    loading.style.display = "none";
    resultsContainer.style.display = "none";

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        formSection.style.display = "none";
        loading.style.display = "block";
        resultsContainer.style.display = "none";

        try {
            const user = localStorage.getItem('user') || '';
            const username = user || "estudiante";

            const response = await fetch(`http://localhost:8000/user/course/${username}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Error al obtener cursos');
            }

            const data = await response.json();
            const cursos = data.cursos || [];
            const cursosAprobados = cursos;

            const body = {
                username: username,
                cursos_aprobados: cursosAprobados
            };
            
            const responseDisponible = await fetch(`http://localhost:4000/cursos/recomendadosNombre`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            });

            if (!responseDisponible.ok) {
                throw new Error('Error al obtener cursos');
            }

            const dataDisponible = await responseDisponible.json();

            const cursosDisponibles = dataDisponible.cursos_disponibles || [];



            const bodyIA = {
                username: username,
                cursos_aprobados: cursosDisponibles
            };
            
            const responseIA = await fetch(`http://localhost:4000/cursos/recomendados`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(bodyIA)
            });

            if (!responseIA.ok) {
                throw new Error('Error al obtener cursos');
            }

            const dataIA = await responseIA.json();

            const recomendacion = dataIA.recomendacion || "No hay recomendaciones disponibles.";

            recommendationsList.innerHTML = "";

            if (recomendacion !== "No hay recomendaciones disponibles.") {
                const cursosHTML = `
                    <h3>Cursos disponibles:</h3>
                    <ul>
                            ${recomendacion}
                        </ul>
                `;
                recommendationsList.innerHTML += cursosHTML;
            }

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

function nuevaConsulta() {
    document.getElementById("formSection").style.display = "block";
    document.getElementById("loading").style.display = "none";
    document.getElementById("resultsContainer").style.display = "none"
}
function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        localStorage.removeItem('user');
        alert('Sesión cerrada correctamente');
        window.location.href = 'login.html';
    }
}

function navigate(section) {
    switch (section) {
        case 'dashboard':
            window.location.href = 'dashboard.html';
            break;
        case 'historial':
            window.location.href = 'historial.html';
            break;
        case 'recomendaciones':
            window.location.href = 'recomendaciones.html';
            break;
        case 'cursos':
            window.location.href = 'cursos.html';
            break;
        default:
            console.warn("Sección no definida:", section);
    }
}

window.onload = function () {
    const user = localStorage.getItem('user') || '';
    if (user.nombre) {
        document.getElementById('userName').textContent = user.nombre;
        document.getElementById('userAvatar').textContent = user.nombre.charAt(0).toUpperCase();
    }

    cargarEstadisticas();
};
async function cargarDatosDashboard() {
    const user = localStorage.getItem('user') || '';
    const username = user || "estudiante";
    document.getElementById('userName').textContent = username
    document.getElementById('userAvatar').textContent = username.charAt(0).toUpperCase();
 
    const creditosAprobadosEl = document.getElementById('creditosAprobados');
    const cursosCompletadosEl = document.getElementById('cursosCompletados');
    const cursosDisponiblesEl = document.getElementById('cursosDisponibles');
    try {
    
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
        const cursosDisponibles = cursos.filter(curso => curso.toLowerCase().includes("disponible"));
        cursosCompletadosEl.textContent = cursosAprobados.length;
        cursosDisponiblesEl.textContent = cursosDisponibles.length;
        const creditosAprobados = cursosAprobados.length * 3;
        creditosAprobadosEl.textContent = creditosAprobados;

    } catch (error) {
        console.error(error);
        cursosCompletadosEl.textContent = 'Error';
    }
}
window.onload = cargarDatosDashboard;
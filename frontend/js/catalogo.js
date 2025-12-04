const cursos = [
    { codigo: "SOF-01", nombre: "Estructuras discretas", creditos: 4, requisito: null, area: "matematicas", nivel: "inicial", cuatrimestre: 1 },
    { codigo: "SOF-02", nombre: "Ingles para las tecnologias I", creditos: 4, requisito: null, area: "idiomas", nivel: "inicial", cuatrimestre: 1 },
    { codigo: "SOF-03", nombre: "Introduccion a la computacion", creditos: 4, requisito: null, area: "general", nivel: "inicial", cuatrimestre: 1 },
    { codigo: "SOF-04", nombre: "Tecnicas de comunicacion", creditos: 4, requisito: null, area: "general", nivel: "inicial", cuatrimestre: 1 },
    { codigo: "SOF-05", nombre: "Calculo I", creditos: 4, requisito: "SOF-01", area: "matematicas", nivel: "intermedio", cuatrimestre: 2 },
    { codigo: "SOF-06", nombre: "Ingles para las tecnologias II", creditos: 4, requisito: "SOF-02", area: "idiomas", nivel: "intermedio", cuatrimestre: 2 },
    { codigo: "SOF-07", nombre: "Investigacion aplicada a las tecnologias", creditos: 4, requisito: "SOF-04", area: "general", nivel: "intermedio", cuatrimestre: 2 },
    { codigo: "SOF-08", nombre: "Programacion I", creditos: 4, requisito: "SOF-03", area: "programacion", nivel: "intermedio", cuatrimestre: 2 },
    { codigo: "SOF-09", nombre: "Calculo II", creditos: 4, requisito: "SOF-05", area: "matematicas", nivel: "intermedio", cuatrimestre: 3 },
    { codigo: "SOF-10", nombre: "Estructuras de datos y algoritmos", creditos: 4, requisito: "SOF-08", area: "programacion", nivel: "intermedio", cuatrimestre: 3 },
    { codigo: "SOF-11", nombre: "Probabilidad y estadistica", creditos: 4, requisito: "SOF-05", area: "matematicas", nivel: "intermedio", cuatrimestre: 3 },
    { codigo: "SOF-12", nombre: "Programacion II", creditos: 4, requisito: "SOF-08", area: "programacion", nivel: "intermedio", cuatrimestre: 3 },
    { codigo: "SOF-13", nombre: "Arquitectura y organizacion de computadores", creditos: 4, requisito: "SOF-12", area: "hardware", nivel: "intermedio", cuatrimestre: 4 },
    { codigo: "SOF-14", nombre: "Bases de datos I", creditos: 4, requisito: "SOF-12", area: "bases_datos", nivel: "intermedio", cuatrimestre: 4 },
    { codigo: "SOF-15", nombre: "Verificacion y validacion de software", creditos: 4, requisito: "SOF-08", area: "ingenieria_software", nivel: "intermedio", cuatrimestre: 4 },
    { codigo: "SOF-16", nombre: "Programacion III", creditos: 4, requisito: "SOF-12", area: "programacion", nivel: "intermedio", cuatrimestre: 4 },
    { codigo: "SOF-17", nombre: "Bases de datos II", creditos: 4, requisito: "SOF-14", area: "bases_datos", nivel: "avanzado", cuatrimestre: 5 },
    { codigo: "SOF-18", nombre: "Programacion IV", creditos: 4, requisito: "SOF-16", area: "programacion", nivel: "avanzado", cuatrimestre: 5 },
    { codigo: "SOF-19", nombre: "Análisis y especificacion de software", creditos: 4, requisito: "SOF-14", area: "ingenieria_software", nivel: "avanzado", cuatrimestre: 5 },
    { codigo: "SOF-20", nombre: "Sistemas operativos", creditos: 4, requisito: "SOF-09", area: "sistemas_operativos", nivel: "avanzado", cuatrimestre: 5 },
    { codigo: "SOF-21", nombre: "Redes de computadoras", creditos: 4, requisito: "SOF-17", area: "redes", nivel: "avanzado", cuatrimestre: 6 },
    { codigo: "SOF-23", nombre: "Lenguajes y paradigmas de programacion", creditos: 4, requisito: "SOF-19", area: "programacion", nivel: "avanzado", cuatrimestre: 6 },
    { codigo: "SOF-24", nombre: "Diseño de software", creditos: 4, requisito: "SOF-19", area: "ingenieria_software", nivel: "avanzado", cuatrimestre: 6 },
    { codigo: "SOF-25", nombre: "Calidad de software", creditos: 4, requisito: "SOF-18", area: "ingenieria_software", nivel: "avanzado", cuatrimestre: 6 },
    { codigo: "SOF-26", nombre: "Diseño de la interaccion humano-computadora", creditos: 4, requisito: "SOF-24", area: "ingenieria_software", nivel: "avanzado", cuatrimestre: 7 },
    { codigo: "SOF-27", nombre: "Topicos avanzados de programacion", creditos: 4, requisito: "SOF-23", area: "programacion", nivel: "avanzado", cuatrimestre: 7 },
    { codigo: "SOF-28", nombre: "Investigacion de operaciones", creditos: 4, requisito: "SOF-09", area: "matematicas", nivel: "avanzado", cuatrimestre: 7 },
    { codigo: "SOF-29", nombre: "Procesos de ingenieria de software", creditos: 4, requisito: "SOF-24", area: "ingenieria_software", nivel: "avanzado", cuatrimestre: 7 },
    { codigo: "SOF-30", nombre: "Arquitectura de software", creditos: 4, requisito: "SOF-29", area: "ingenieria_software", nivel: "avanzado", cuatrimestre: 8 },
    { codigo: "SOF-31", nombre: "Inteligencia artificial aplicada", creditos: 4, requisito: "SOF-29", area: "programacion", nivel: "avanzado", cuatrimestre: 8 },
    { codigo: "SOF-32", nombre: "Electiva I", creditos: 4, requisito: "SOF-27", area: "general", nivel: "avanzado", cuatrimestre: 8 },
    { codigo: "SOF-33", nombre: "Administracion de proyectos informaticos", creditos: 4, requisito: "SOF-29", area: "ingenieria_software", nivel: "avanzado", cuatrimestre: 8 },
    { codigo: "SOF-34", nombre: "Computacion y sociedad", creditos: 4, requisito: "SOF-33", area: "general", nivel: "avanzado", cuatrimestre: 9 },
    { codigo: "SOF-35", nombre: "Electiva II", creditos: 4, requisito: "SOF-30", area: "general", nivel: "avanzado", cuatrimestre: 9 },
    { codigo: "SOF-36", nombre: "Implementacion y mantenimiento de software", creditos: 4, requisito: "SOF-30", area: "ingenieria_software", nivel: "avanzado", cuatrimestre: 9 },
    { codigo: "SOF-37", nombre: "Seguridad informatica", creditos: 4, requisito: "SOF-29", area: "seguridad", nivel: "avanzado", cuatrimestre: 9 }
];

const areaNombres = {
    matematicas: "Matemáticas",
    idiomas: "Idiomas",
    general: "General",
    programacion: "Programación",
    hardware: "Hardware",
    bases_datos: "Bases de Datos",
    ingenieria_software: "Ingeniería de Software",
    sistemas_operativos: "Sistemas Operativos",
    redes: "Redes",
    seguridad: "Seguridad"
};

const nivelNombres = {
    inicial: "Inicial",
    intermedio: "Intermedio",
    avanzado: "Avanzado"
};

const areaColores = {
    matematicas: "#e74c3c",
    idiomas: "#9b59b6",
    general: "#95a5a6",
    programacion: "#3498db",
    hardware: "#e67e22",
    bases_datos: "#27ae60",
    ingenieria_software: "#2980b9",
    sistemas_operativos: "#8e44ad",
    redes: "#16a085",
    seguridad: "#c0392b"
};

const searchInput = document.getElementById('searchInput');
const nivelFilter = document.getElementById('nivelFilter');
const areaFilter = document.getElementById('areaFilter');
const coursesGrid = document.getElementById('coursesGrid');
const resultCount = document.getElementById('resultCount');
const modalDetalle = document.getElementById('modalDetalle');
const modalBody = document.getElementById('modalBody');

document.addEventListener('DOMContentLoaded', () => {
    poblarFiltroAreas();
    renderizarCursos(cursos);
    agregarEventListeners();
});

function poblarFiltroAreas() {
    const areasUnicas = [...new Set(cursos.map(c => c.area))];
    areasUnicas.sort((a, b) => areaNombres[a].localeCompare(areaNombres[b]));
    
    areasUnicas.forEach(area => {
        const option = document.createElement('option');
        option.value = area;
        option.textContent = areaNombres[area];
        areaFilter.appendChild(option);
    });
}

function agregarEventListeners() {
    searchInput.addEventListener('input', filtrarCursos);
    nivelFilter.addEventListener('change', filtrarCursos);
    areaFilter.addEventListener('change', filtrarCursos);
}

function filtrarCursos() {
    const busqueda = searchInput.value.toLowerCase().trim();
    const nivelSeleccionado = nivelFilter.value;
    const areaSeleccionada = areaFilter.value;

    const cursosFiltrados = cursos.filter(curso => {
        const coincideBusqueda = busqueda === '' || 
            curso.nombre.toLowerCase().includes(busqueda) ||
            curso.codigo.toLowerCase().includes(busqueda);

        const coincideNivel = nivelSeleccionado === '' || 
            curso.nivel === nivelSeleccionado;

        const coincideArea = areaSeleccionada === '' || 
            curso.area === areaSeleccionada;

        return coincideBusqueda && coincideNivel && coincideArea;
    });

    renderizarCursos(cursosFiltrados);
}

function renderizarCursos(listaCursos) {
    coursesGrid.innerHTML = '';
    resultCount.textContent = listaCursos.length;

    if (listaCursos.length === 0) {
        coursesGrid.innerHTML = `
            <div class="no-results">
                <p>No se encontraron cursos con los filtros seleccionados.</p>
                <button onclick="limpiarFiltros()" class="btn-limpiar">Limpiar filtros</button>
            </div>
        `;
        return;
    }

    listaCursos.forEach(curso => {
        const card = crearTarjetaCurso(curso);
        coursesGrid.appendChild(card);
    });
}

function crearTarjetaCurso(curso) {
    const card = document.createElement('div');
    card.className = 'course-card';
    card.onclick = () => mostrarDetalle(curso);

    const colorArea = areaColores[curso.area] || '#3498db';

    card.innerHTML = `
        <div class="course-header" style="border-left: 4px solid ${colorArea}">
            <span class="course-code">${curso.codigo}</span>
            <span class="course-level nivel-${curso.nivel}">${nivelNombres[curso.nivel]}</span>
        </div>
        <h3 class="course-name">${curso.nombre}</h3>
        <div class="course-info">
            <span class="info-badge area-badge" style="background-color: ${colorArea}20; color: ${colorArea}">
                ${areaNombres[curso.area]}
            </span>
            <span class="info-badge credits-badge">
                ${curso.creditos} créditos
            </span>
        </div>
        <div class="course-footer">
            <span class="cuatrimestre">Cuatrimestre ${curso.cuatrimestre}</span>
            ${curso.requisito ? `<span class="requisito">Req: ${curso.requisito}</span>` : '<span class="requisito sin-req">Sin requisitos</span>'}
        </div>
    `;

    return card;
}

function mostrarDetalle(curso) {
    const colorArea = areaColores[curso.area] || '#3498db';
    const cursoRequisito = curso.requisito ? cursos.find(c => c.codigo === curso.requisito) : null;
    const cursosQueRequieren = cursos.filter(c => c.requisito === curso.codigo);

    modalBody.innerHTML = `
        <div class="modal-header" style="border-bottom: 3px solid ${colorArea}">
            <span class="modal-code">${curso.codigo}</span>
            <h2 class="modal-title">${curso.nombre}</h2>
        </div>
        
        <div class="modal-details">
            <div class="detail-row">
                <span class="detail-label">Nivel:</span>
                <span class="detail-value nivel-${curso.nivel}">${nivelNombres[curso.nivel]}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Área:</span>
                <span class="detail-value" style="color: ${colorArea}">${areaNombres[curso.area]}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Créditos:</span>
                <span class="detail-value">${curso.creditos}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Cuatrimestre:</span>
                <span class="detail-value">${curso.cuatrimestre}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Requisito:</span>
                <span class="detail-value">
                    ${cursoRequisito 
                        ? `<a href="#" onclick="mostrarDetalle(cursos.find(c => c.codigo === '${curso.requisito}')); return false;">${curso.requisito} - ${cursoRequisito.nombre}</a>` 
                        : 'Ninguno'}
                </span>
            </div>
        </div>

        ${cursosQueRequieren.length > 0 ? `
            <div class="cursos-dependientes">
                <h4>Cursos que requieren este curso:</h4>
                <ul>
                    ${cursosQueRequieren.map(c => `
                        <li>
                            <a href="#" onclick="mostrarDetalle(cursos.find(curso => curso.codigo === '${c.codigo}')); return false;">
                                ${c.codigo} - ${c.nombre}
                            </a>
                        </li>
                    `).join('')}
                </ul>
            </div>
        ` : ''}
    `;

    modalDetalle.style.display = 'flex';
}

function cerrarModal() {
    modalDetalle.style.display = 'none';
}

window.onclick = (event) => {
    if (event.target === modalDetalle) {
        cerrarModal();
    }
};

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        cerrarModal();
    }
});

function limpiarFiltros() {
    searchInput.value = '';
    nivelFilter.value = '';
    areaFilter.value = '';
    renderizarCursos(cursos);
}

function navigate(page) {
    window.location.href = page + '.html';
}

function logout() {
    window.location.href = 'index.html';
}
const cursosData = [
    {
        codigo: 'SOF-01',
        nombre: 'Introducción a la Programación',
        creditos: 3,
        nivel: 'inicial',
        area: 'programacion',
        descripcion: 'Fundamentos de la programación usando Python. Variables, estructuras de control, funciones básicas.',
        requisitos: [],
        objetivos: ['Comprender conceptos básicos de programación', 'Desarrollar algoritmos simples', 'Resolver problemas computacionales']
    },
    {
        codigo: 'SOF-02',
        nombre: 'Estructuras de Datos',
        creditos: 3,
        nivel: 'intermedio',
        area: 'programacion',
        descripcion: 'Listas, pilas, colas, árboles y grafos. Análisis de complejidad algorítmica.',
        requisitos: ['SOF-01'],
        objetivos: ['Implementar estructuras de datos', 'Analizar eficiencia de algoritmos', 'Resolver problemas con estructuras avanzadas']
    },
    {
        codigo: 'SOF-03',
        nombre: 'Algoritmos',
        creditos: 3,
        nivel: 'intermedio',
        area: 'programacion',
        descripcion: 'Técnicas de diseño algorítmico: divide y vencerás, programación dinámica, algoritmos voraces.',
        requisitos: ['SOF-02'],
        objetivos: ['Diseñar algoritmos eficientes', 'Optimizar soluciones', 'Aplicar técnicas avanzadas']
    },
    {
        codigo: 'SOF-04',
        nombre: 'Bases de Datos I',
        creditos: 3,
        nivel: 'intermedio',
        area: 'bases-datos',
        descripcion: 'Modelo relacional, SQL, normalización, diseño de bases de datos relacionales.',
        requisitos: ['SOF-01'],
        objetivos: ['Diseñar bases de datos relacionales', 'Escribir consultas SQL complejas', 'Normalizar esquemas']
    },
    {
        codigo: 'SOF-05',
        nombre: 'Bases de Datos II',
        creditos: 3,
        nivel: 'avanzado',
        area: 'bases-datos',
        descripcion: 'Transacciones, concurrencia, optimización, bases de datos distribuidas y NoSQL.',
        requisitos: ['SOF-04'],
        objetivos: ['Gestionar transacciones', 'Optimizar consultas', 'Trabajar con bases NoSQL']
    },
    {
        codigo: 'SOF-06',
        nombre: 'Desarrollo Web',
        creditos: 3,
        nivel: 'intermedio',
        area: 'programacion',
        descripcion: 'HTML, CSS, JavaScript, frameworks modernos, diseño responsivo y APIs REST.',
        requisitos: ['SOF-01'],
        objetivos: ['Crear aplicaciones web', 'Implementar APIs REST', 'Desarrollar interfaces responsivas']
    },
    {
        codigo: 'SOF-07',
        nombre: 'Programación Orientada a Objetos',
        creditos: 3,
        nivel: 'intermedio',
        area: 'programacion',
        descripcion: 'Clases, herencia, polimorfismo, encapsulación, patrones de diseño orientados a objetos.',
        requisitos: ['SOF-02'],
        objetivos: ['Aplicar principios POO', 'Implementar patrones de diseño', 'Desarrollar sistemas modulares']
    },
    {
        codigo: 'SOF-08',
        nombre: 'Ingeniería de Software',
        creditos: 4,
        nivel: 'avanzado',
        area: 'software',
        descripcion: 'Metodologías ágiles, análisis de requisitos, arquitectura de software, pruebas y calidad.',
        requisitos: ['SOF-07'],
        objetivos: ['Gestionar proyectos software', 'Aplicar metodologías ágiles', 'Garantizar calidad del software']
    },
    {
        codigo: 'RED-01',
        nombre: 'Redes de Computadoras',
        creditos: 3,
        nivel: 'intermedio',
        area: 'redes',
        descripcion: 'Modelo OSI, TCP/IP, protocolos de red, configuración de routers y switches.',
        requisitos: ['SOF-01'],
        objetivos: ['Comprender arquitectura de redes', 'Configurar dispositivos de red', 'Resolver problemas de conectividad']
    },
    {
        codigo: 'RED-02',
        nombre: 'Seguridad en Redes',
        creditos: 3,
        nivel: 'avanzado',
        area: 'redes',
        descripcion: 'Criptografía, firewalls, VPNs, detección de intrusos, seguridad en aplicaciones web.',
        requisitos: ['RED-01'],
        objetivos: ['Implementar medidas de seguridad', 'Detectar vulnerabilidades', 'Proteger infraestructuras']
    },
    {
        codigo: 'SOF-09',
        nombre: 'Inteligencia Artificial',
        creditos: 4,
        nivel: 'avanzado',
        area: 'programacion',
        descripcion: 'Búsqueda heurística, machine learning, redes neuronales, procesamiento de lenguaje natural.',
        requisitos: ['SOF-03', 'SOF-02'],
        objetivos: ['Implementar algoritmos de IA', 'Entrenar modelos ML', 'Aplicar IA a problemas reales']
    },
    {
        codigo: 'SOF-10',
        nombre: 'Sistemas Operativos',
        creditos: 3,
        nivel: 'intermedio',
        area: 'programacion',
        descripcion: 'Procesos, hilos, gestión de memoria, sistemas de archivos, virtualización.',
        requisitos: ['SOF-02'],
        objetivos: ['Comprender funcionamiento de SO', 'Gestionar recursos del sistema', 'Programar a nivel de sistema']
    },
    {
        codigo: 'SOF-11',
        nombre: 'Arquitectura de Computadoras',
        creditos: 3,
        nivel: 'inicial',
        area: 'programacion',
        descripcion: 'Organización de hardware, lenguaje ensamblador, jerarquía de memoria, procesadores.',
        requisitos: [],
        objetivos: ['Entender arquitectura de computadoras', 'Programar en ensamblador', 'Optimizar código']
    },
    {
        codigo: 'SOF-12',
        nombre: 'Computación en la Nube',
        creditos: 3,
        nivel: 'avanzado',
        area: 'redes',
        descripcion: 'AWS, Azure, Docker, Kubernetes, arquitecturas serverless, microservicios.',
        requisitos: ['RED-01', 'SOF-06'],
        objetivos: ['Desplegar aplicaciones en la nube', 'Trabajar con contenedores', 'Diseñar arquitecturas cloud']
    },
    {
        codigo: 'SOF-13',
        nombre: 'Desarrollo Móvil',
        creditos: 3,
        nivel: 'avanzado',
        area: 'programacion',
        descripcion: 'Android, iOS, React Native, Flutter, diseño de interfaces móviles.',
        requisitos: ['SOF-06', 'SOF-07'],
        objetivos: ['Crear aplicaciones móviles', 'Publicar apps', 'Optimizar UX móvil']
    }
];

let cursosFiltrados = [...cursosData];

window.onload = function() {
    renderizarCursos(cursosData);
    
    document.getElementById('searchInput').addEventListener('input', filtrarCursos);
    document.getElementById('nivelFilter').addEventListener('change', filtrarCursos);
    document.getElementById('areaFilter').addEventListener('change', filtrarCursos);
};

function renderizarCursos(cursos) {
    const grid = document.getElementById('coursesGrid');
    grid.innerHTML = '';

    if (cursos.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>No se encontraron cursos</h3>
                <p>Intenta ajustar los filtros de búsqueda</p>
            </div>
        `;
        return;
    }

    cursos.forEach(curso => {
        const card = document.createElement('div');
        card.className = 'course-card';
        card.onclick = () => verDetalle(curso);

        const requisitosHTML = curso.requisitos.length > 0
            ? `<div class="course-requirements">
                 <h4>📋 Requisitos:</h4>
                 <ul>${curso.requisitos.map(req => `<li>${req}</li>`).join('')}</ul>
               </div>`
            : `<div class="no-requirements">✅ Sin requisitos previos</div>`;

        card.innerHTML = `
            <div class="course-header">
                <span class="course-code">${curso.codigo}</span>
                <span class="course-credits">${curso.creditos} créditos</span>
            </div>
            <h3 class="course-title">${curso.nombre}</h3>
            <p class="course-description">${curso.descripcion}</p>
            <div class="course-meta">
                <span class="meta-item">📊 <span class="level-badge level-${curso.nivel}">${curso.nivel}</span></span>
                <span class="meta-item">🎯 ${curso.area}</span>
            </div>
            ${requisitosHTML}
            <div class="course-actions">
                <button class="btn-primary" onclick="event.stopPropagation(); agregarACursar('${curso.codigo}')">
                    + Agregar a Cursar
                </button>
                <button class="btn-secondary" onclick="event.stopPropagation(); verDetalle(cursosData.find(c => c.codigo === '${curso.codigo}'))">
                    Ver Detalles
                </button>
            </div>
        `;

        grid.appendChild(card);
    });

    document.getElementById('resultCount').textContent = cursos.length;
}

function filtrarCursos() {
    const busqueda = document.getElementById('searchInput').value.toLowerCase();
    const nivel = document.getElementById('nivelFilter').value;
    const area = document.getElementById('areaFilter').value;

    cursosFiltrados = cursosData.filter(curso => {
        const matchBusqueda = !busqueda || 
            curso.nombre.toLowerCase().includes(busqueda) || 
            curso.codigo.toLowerCase().includes(busqueda);
        
        const matchNivel = !nivel || curso.nivel === nivel;
        const matchArea = !area || curso.area === area;

        return matchBusqueda && matchNivel && matchArea;
    });

    renderizarCursos(cursosFiltrados);
}

function verDetalle(curso) {
    const modal = document.getElementById('modalDetalle');
    const modalBody = document.getElementById('modalBody');

    const requisitosHTML = curso.requisitos.length > 0
        ? `<h4>📋 Requisitos Previos:</h4><ul>${curso.requisitos.map(req => `<li>${req}</li>`).join('')}</ul>`
        : `<p class="no-requirements">✅ Este curso no tiene requisitos previos</p>`;

    modalBody.innerHTML = `
        <h2 class="modal-header">${curso.codigo} - ${curso.nombre}</h2>
        <div class="modal-body">
            <p><strong>📚 Créditos:</strong> ${curso.creditos}</p>
            <p><strong>📊 Nivel:</strong> <span class="level-badge level-${curso.nivel}">${curso.nivel}</span></p>
            <p><strong>🎯 Área:</strong> ${curso.area}</p>
            <br>
            <h4>📖 Descripción:</h4>
            <p>${curso.descripcion}</p>
            <br>
            ${requisitosHTML}
            <br>
            <h4>🎯 Objetivos del curso:</h4>
            <ul>${curso.objetivos.map(obj => `<li>${obj}</li>`).join('')}</ul>
        </div>
    `;

    modal.classList.add('active');
}

function cerrarModal() {
    document.getElementById('modalDetalle').classList.remove('active');
}

function agregarACursar(codigo) {
    alert(`El curso ${codigo} ha sido agregado a tu lista de interés. Ve a "Mi Historial" para registrarlo oficialmente.`);
}

function navigate(page) {
    window.location.href = `${page}.html`;
}

function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        alert('Sesión cerrada correctamente');
        window.location.href = 'login.html';
    }
}

window.onclick = function(event) {
    const modal = document.getElementById('modalDetalle');
    if (event.target === modal) {
        cerrarModal();
    }
};
const DB_KEY = 'historial_academico_uia';

function getCreditosTotales() {
    return cursos.reduce((sum, c) => sum + c.creditos, 0);
}

function generarDatosIniciales() {
    const historial = {};
    
    cursos.forEach(curso => {
        historial[curso.codigo] = {
            estado: 'pendiente', 
            progreso: 0 
        };
    });
    
    return {
        historial: historial,
        creditosTotales: getCreditosTotales()
    };
}

function initDB() {
    if (!localStorage.getItem(DB_KEY)) {
        localStorage.setItem(DB_KEY, JSON.stringify(generarDatosIniciales()));
    }
    return getDB();
}

function getDB() {
    return JSON.parse(localStorage.getItem(DB_KEY));
}

function saveDB(data) {
    localStorage.setItem(DB_KEY, JSON.stringify(data));
}

function resetDB() {
    localStorage.setItem(DB_KEY, JSON.stringify(generarDatosIniciales()));
    location.reload();
}

function obtenerCursoCompleto(codigo) {
    const cursoCatalogo = cursos.find(c => c.codigo === codigo);
    if (!cursoCatalogo) return null;
    
    const db = getDB();
    const estadoCurso = db.historial[codigo] || { estado: 'pendiente', progreso: 0 };
    
    return {
        ...cursoCatalogo,
        ...estadoCurso
    };
}

function obtenerTodosCursos() {
    return cursos.map(curso => obtenerCursoCompleto(curso.codigo));
}

function requisitosCumplidos(codigo) {
    const curso = cursos.find(c => c.codigo === codigo);
    if (!curso || !curso.requisito) return true;
    
    const db = getDB();
    const estadoRequisito = db.historial[curso.requisito];
    
    return estadoRequisito && estadoRequisito.estado === 'aprobado';
}

function obtenerCursosDisponibles() {
    const todos = obtenerTodosCursos();
    
    return todos.filter(c => {
        if (c.estado !== 'pendiente') return false;
        
        return requisitosCumplidos(c.codigo);
    });
}

function obtenerCursosBloqueados() {
    const todos = obtenerTodosCursos();
    
    return todos.filter(c => {
        if (c.estado !== 'pendiente') return false;
        return !requisitosCumplidos(c.codigo);
    });
}

function obtenerCursosPorEstado(estado) {
    const todos = obtenerTodosCursos();
    return todos.filter(c => c.estado === estado);
}

function actualizarEstadoCurso(codigo, nuevoEstado, progreso = 0) {
    const db = getDB();
    
    if (!db.historial[codigo]) {
        db.historial[codigo] = { estado: 'pendiente', progreso: 0 };
    }
    
    db.historial[codigo].estado = nuevoEstado;
    db.historial[codigo].progreso = nuevoEstado === 'en-curso' ? progreso : 0;
    
    saveDB(db);
    return obtenerCursoCompleto(codigo);
}

function actualizarProgreso(codigo, progreso) {
    const db = getDB();
    
    if (db.historial[codigo] && db.historial[codigo].estado === 'en-curso') {
        db.historial[codigo].progreso = Math.min(100, Math.max(0, progreso));
        saveDB(db);
    }
    
    return obtenerCursoCompleto(codigo);
}

function calcularEstadisticas() {
    const todos = obtenerTodosCursos();
    const creditosTotales = getCreditosTotales();
    
    const aprobados = todos.filter(c => c.estado === 'aprobado');
    const enCurso = todos.filter(c => c.estado === 'en-curso');
    const disponibles = obtenerCursosDisponibles();
    const bloqueados = obtenerCursosBloqueados();
    
    const creditosAprobados = aprobados.reduce((sum, c) => sum + c.creditos, 0);
    const creditosEnCurso = enCurso.reduce((sum, c) => sum + c.creditos, 0);
    
    return {
        creditosAprobados,
        creditosEnCurso,
        cursosAprobados: aprobados.length,
        cursosEnCurso: enCurso.length,
        cursosDisponibles: disponibles.length,
        cursosBloqueados: bloqueados.length,
        totalCursos: todos.length,
        progreso: Math.round((creditosAprobados / creditosTotales) * 100),
        creditosTotales: creditosTotales
    };
}

let tabActual = 'aprobados';

document.addEventListener('DOMContentLoaded', () => {
    initDB();
    renderizarTodo();
    configurarEventos();
});

function renderizarTodo() {
    renderizarEstadisticas();
    renderizarTablas();
    actualizarSelectCursos();
}

function renderizarEstadisticas() {
    const stats = calcularEstadisticas();
    
    document.getElementById('totalCreditos').textContent = stats.creditosAprobados;
    document.getElementById('cursosAprobados').textContent = stats.cursosAprobados;
    document.getElementById('cursosEnCurso').textContent = stats.cursosEnCurso;
    document.getElementById('promedio').textContent = stats.progreso + '%';
    
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
        progressFill.style.width = `${Math.max(stats.progreso, 5)}%`;
        progressFill.textContent = `${stats.creditosAprobados} / ${stats.creditosTotales} créditos`;
    }
    
    const progressText = document.querySelector('.content-section p');
    if (progressText) {
        progressText.textContent = `Has completado el ${stats.progreso}% de tu carrera`;
    }
}

function renderizarTablas() {
    renderizarTablaCursos('aprobados');
    renderizarTablaCursos('en-curso');
    renderizarTablaCursos('pendientes');
    renderizarTablaCursos('bloqueados');
}

function renderizarTablaCursos(tipo) {
    let cursosList;
    let tbody;
    
    switch(tipo) {
        case 'aprobados':
            cursosList = obtenerCursosPorEstado('aprobado');
            tbody = document.querySelector('#aprobados tbody');
            break;
        case 'en-curso':
            cursosList = obtenerCursosPorEstado('en-curso');
            tbody = document.querySelector('#en-curso tbody');
            break;
        case 'pendientes':
            // Solo cursos disponibles para matricular
            cursosList = obtenerCursosDisponibles();
            tbody = document.querySelector('#pendientes tbody');
            break;
        case 'bloqueados':
            // Cursos con requisitos faltantes
            cursosList = obtenerCursosBloqueados();
            tbody = document.querySelector('#bloqueados tbody');
            break;
    }
    
    if (!tbody) return;
    
    cursosList.sort((a, b) => a.cuatrimestre - b.cuatrimestre);
    
    if (cursosList.length === 0) {
        const colspan = tipo === 'aprobados' ? 5 : tipo === 'en-curso' ? 6 : tipo === 'pendientes' ? 5 : 6;
        tbody.innerHTML = `
            <tr>
                <td colspan="${colspan}">
                    <div class="empty-state">
                        <div class="empty-icon">${tipo === 'bloqueados' ? '🔒' : '📚'}</div>
                        <div class="empty-title">
                            ${tipo === 'aprobados' ? 'No hay cursos aprobados' : 
                              tipo === 'en-curso' ? 'No hay cursos en curso' :
                              tipo === 'pendientes' ? 'No hay cursos disponibles' :
                              'No hay cursos bloqueados'}
                        </div>
                        <div class="empty-message">
                            ${tipo === 'aprobados' ? 'Aún no has aprobado ningún curso' : 
                              tipo === 'en-curso' ? 'No tienes cursos en curso actualmente' :
                              tipo === 'pendientes' ? '¡Excelente! Estás al día con tu carrera' :
                              'Todos los requisitos están cumplidos'}
                        </div>
                    </div>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = cursosList.map(curso => generarFilaCurso(curso, tipo)).join('');
}

function generarFilaCurso(curso, tipo) {
    const colorArea = areaColores[curso.area] || '#3498db';
    const areaBadge = `<span class="badge" style="background-color: ${colorArea}20; color: ${colorArea}">${areaNombres[curso.area]}</span>`;
    
    switch(tipo) {
        case 'aprobados':
            return `
                <tr data-codigo="${curso.codigo}">
                    <td><strong>${curso.codigo}</strong></td>
                    <td>${curso.nombre}</td>
                    <td>${areaBadge}</td>
                    <td>${curso.creditos}</td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn-secondary btn-icon" onclick="verDetalle('${curso.codigo}')" title="Ver detalle">👁️</button>
                            <button class="btn-danger btn-icon" onclick="quitarAprobado('${curso.codigo}')" title="Quitar de aprobados">↩️</button>
                        </div>
                    </td>
                </tr>
            `;
        case 'en-curso':
            return `
                <tr data-codigo="${curso.codigo}">
                    <td><strong>${curso.codigo}</strong></td>
                    <td>${curso.nombre}</td>
                    <td>${areaBadge}</td>
                    <td>${curso.creditos}</td>
                    <td>
                        <div class="progress-bar" style="height: 22px; width: 120px;">
                            <div class="progress-fill" style="width: ${curso.progreso || 0}%;">${curso.progreso || 0}%</div>
                        </div>
                    </td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn-secondary btn-icon" onclick="verDetalle('${curso.codigo}')" title="Ver detalle">👁️</button>
                            <button class="btn-secondary btn-icon" onclick="editarProgreso('${curso.codigo}')" title="Editar progreso">📝</button>
                            <button class="btn-success btn-icon" onclick="marcarAprobado('${curso.codigo}')" title="Marcar como aprobado">✓</button>
                        </div>
                    </td>
                </tr>
            `;
        case 'pendientes':
            return `
                <tr data-codigo="${curso.codigo}">
                    <td><strong>${curso.codigo}</strong></td>
                    <td>${curso.nombre}</td>
                    <td>${areaBadge}</td>
                    <td>${curso.creditos}</td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn-secondary btn-icon" onclick="verDetalle('${curso.codigo}')" title="Ver detalle">👁️</button>
                            <button class="btn-success btn-icon" onclick="iniciarCurso('${curso.codigo}')" title="Iniciar curso">▶️</button>
                        </div>
                    </td>
                </tr>
            `;
        case 'bloqueados':
            const cursoRequisito = obtenerCursoCompleto(curso.requisito);
            const requisitoNombre = cursoRequisito ? `${curso.requisito} - ${cursoRequisito.nombre}` : curso.requisito;
            return `
                <tr data-codigo="${curso.codigo}" class="bloqueado">
                    <td><strong>${curso.codigo}</strong></td>
                    <td>${curso.nombre}</td>
                    <td>${areaBadge}</td>
                    <td>${curso.creditos}</td>
                    <td>
                        <span class="badge badge-danger">Falta: ${curso.requisito}</span>
                    </td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn-secondary btn-icon" onclick="verDetalle('${curso.codigo}')" title="Ver detalle">👁️</button>
                            <button class="btn-secondary btn-icon" disabled title="Faltan requisitos">🔒</button>
                        </div>
                    </td>
                </tr>
            `;
    }
}

function abrirModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

function cerrarModal(modalId) {
    const modal = modalId ? document.getElementById(modalId) : document.querySelector('.modal.show');
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
        
        const form = modal.querySelector('form');
        if (form) form.reset();
    }
}

function abrirModalAgregar() {
    actualizarSelectCursos();
    abrirModal('modalCurso');
}

function verDetalle(codigo) {
    const curso = obtenerCursoCompleto(codigo);
    if (!curso) return;
    
    const colorArea = areaColores[curso.area] || '#3498db';
    const cursoRequisito = curso.requisito ? obtenerCursoCompleto(curso.requisito) : null;
    const cursosQueRequieren = cursos.filter(c => c.requisito === codigo);
    const tieneRequisitosCompletos = requisitosCumplidos(codigo);
    
    const estadoTexto = {
        'aprobado': 'Aprobado',
        'en-curso': 'En Curso',
        'pendiente': tieneRequisitosCompletos ? 'Disponible' : 'Faltan Requisitos'
    };
    
    const badgeClass = {
        'aprobado': 'badge-success',
        'en-curso': 'badge-warning',
        'pendiente': tieneRequisitosCompletos ? 'badge-info' : 'badge-danger'
    };
    
    const modalBody = document.querySelector('#modalDetalle .modal-body');
    if (modalBody) {
        modalBody.innerHTML = `
            <div class="detail-grid">
                <div class="detail-item">
                    <div class="detail-label">Código</div>
                    <div class="detail-value">${curso.codigo}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Créditos</div>
                    <div class="detail-value large">${curso.creditos}</div>
                </div>
                <div class="detail-item full-width">
                    <div class="detail-label">Nombre del Curso</div>
                    <div class="detail-value">${curso.nombre}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Área</div>
                    <div class="detail-value">
                        <span class="badge" style="background-color: ${colorArea}20; color: ${colorArea}">${areaNombres[curso.area]}</span>
                    </div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Nivel</div>
                    <div class="detail-value">${nivelNombres[curso.nivel]}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Cuatrimestre</div>
                    <div class="detail-value large">${curso.cuatrimestre}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Estado</div>
                    <div class="detail-value">
                        <span class="badge ${badgeClass[curso.estado]}">${estadoTexto[curso.estado]}</span>
                    </div>
                </div>
                <div class="detail-item full-width">
                    <div class="detail-label">Requisito</div>
                    <div class="detail-value">
                        ${cursoRequisito ? 
                            `<a href="#" onclick="verDetalle('${curso.requisito}'); return false;" style="color: ${colorArea}; text-decoration: none;">
                                ${curso.requisito} - ${cursoRequisito.nombre}
                            </a>
                            ${cursoRequisito.estado === 'aprobado' ? 
                                '<span class="badge badge-success" style="margin-left: 8px;">✓ Completado</span>' : 
                                '<span class="badge badge-danger" style="margin-left: 8px;">✗ Pendiente</span>'}` : 
                            'Ninguno'}
                    </div>
                </div>
                ${curso.estado === 'en-curso' ? `
                <div class="detail-item full-width">
                    <div class="detail-label">Progreso</div>
                    <div class="progress-bar" style="margin-top: 8px;">
                        <div class="progress-fill" style="width: ${curso.progreso}%;">${curso.progreso}%</div>
                    </div>
                </div>
                ` : ''}
                ${cursosQueRequieren.length > 0 ? `
                <div class="detail-item full-width">
                    <div class="detail-label">Cursos que requieren este curso</div>
                    <div class="detail-value" style="font-size: 14px; font-weight: normal;">
                        ${cursosQueRequieren.map(c => 
                            `<a href="#" onclick="verDetalle('${c.codigo}'); return false;" style="color: ${areaColores[c.area]}; text-decoration: none; display: block; margin: 4px 0;">
                                ${c.codigo} - ${c.nombre}
                            </a>`
                        ).join('')}
                    </div>
                </div>
                ` : ''}
            </div>
        `;
    }
    
    abrirModal('modalDetalle');
}

function confirmarAccion(titulo, mensaje, onConfirm) {
    const modalBody = document.querySelector('#modalConfirmar .modal-body');
    if (modalBody) {
        modalBody.innerHTML = `
            <div class="confirm-dialog">
                <div class="confirm-icon">⚠️</div>
                <div class="confirm-title">${titulo}</div>
                <div class="confirm-message">${mensaje}</div>
            </div>
        `;
    }
    
    document.getElementById('modalConfirmar').dataset.onConfirm = 'pending';
    window.confirmarCallback = onConfirm;
    
    abrirModal('modalConfirmar');
}

function ejecutarConfirmacion() {
    if (window.confirmarCallback) {
        window.confirmarCallback();
        window.confirmarCallback = null;
    }
    cerrarModal('modalConfirmar');
}

function actualizarSelectCursos() {
    const select = document.getElementById('cursoSelect');
    if (!select) return;
    
    const cursosDisponibles = obtenerCursosDisponibles();
    
    cursosDisponibles.sort((a, b) => a.cuatrimestre - b.cuatrimestre);
    
    select.innerHTML = '<option value="">Selecciona un curso</option>' +
        cursosDisponibles.map(c => 
            `<option value="${c.codigo}">${c.codigo} - ${c.nombre} (Cuatri ${c.cuatrimestre})</option>`
        ).join('');
}

function iniciarCurso(codigo) {
    const curso = obtenerCursoCompleto(codigo);
    if (!curso || curso.estado !== 'pendiente') return;
    
    if (!requisitosCumplidos(codigo)) {
        mostrarToast('error', 'No disponible', 'Este curso tiene requisitos pendientes');
        return;
    }
    
    actualizarEstadoCurso(codigo, 'en-curso', 0);
    mostrarToast('success', 'Curso iniciado', `Has comenzado ${curso.codigo} - ${curso.nombre}`);
    renderizarTodo();
    cambiarTab('en-curso');
}

function marcarAprobado(codigo) {
    const curso = obtenerCursoCompleto(codigo);
    if (!curso) return;
    
    confirmarAccion(
        '¿Marcar como aprobado?',
        `¿Confirmas que has aprobado <strong>${curso.codigo} - ${curso.nombre}</strong>?`,
        () => {
            actualizarEstadoCurso(codigo, 'aprobado');
            mostrarToast('success', '¡Felicidades!', `Has aprobado ${curso.codigo}`);
            renderizarTodo();
            cambiarTab('aprobados');
        }
    );
}

function quitarAprobado(codigo) {
    const curso = obtenerCursoCompleto(codigo);
    if (!curso) return;
    
    const cursosDependientes = cursos.filter(c => c.requisito === codigo);
    const dependientesAprobados = cursosDependientes.filter(c => {
        const estado = obtenerCursoCompleto(c.codigo);
        return estado && (estado.estado === 'aprobado' || estado.estado === 'en-curso');
    });
    
    let mensajeExtra = '';
    if (dependientesAprobados.length > 0) {
        mensajeExtra = `<br><br><strong>⚠️ Atención:</strong> Los siguientes cursos dependen de este y también serán afectados:<br>
            ${dependientesAprobados.map(c => `• ${c.codigo} - ${c.nombre}`).join('<br>')}`;
    }
    
    confirmarAccion(
        '¿Quitar de aprobados?',
        `¿Seguro que deseas quitar <strong>${curso.codigo} - ${curso.nombre}</strong> de tus cursos aprobados?${mensajeExtra}`,
        () => {
            actualizarEstadoCurso(codigo, 'pendiente');
            mostrarToast('warning', 'Curso movido', `${curso.codigo} ha sido movido a pendientes`);
            renderizarTodo();
        }
    );
}

function editarProgreso(codigo) {
    const curso = obtenerCursoCompleto(codigo);
    if (!curso || curso.estado !== 'en-curso') return;
    
    const modalBody = document.querySelector('#modalProgreso .modal-body');
    if (modalBody) {
        modalBody.innerHTML = `
            <p style="margin-bottom: 20px; color: #666;">
                Actualiza el progreso de <strong>${curso.codigo} - ${curso.nombre}</strong>
            </p>
            <div class="form-group">
                <label>Progreso (%)</label>
                <input type="range" id="progresoSlider" class="form-control" min="0" max="100" value="${curso.progreso || 0}" 
                    oninput="document.getElementById('progresoValor').textContent = this.value + '%'"
                    style="padding: 0;">
                <div style="text-align: center; font-size: 24px; font-weight: bold; margin-top: 10px; color: #f4c430;">
                    <span id="progresoValor">${curso.progreso || 0}%</span>
                </div>
            </div>
        `;
    }
    
    document.getElementById('modalProgreso').dataset.cursoId = codigo;
    abrirModal('modalProgreso');
}

function guardarProgreso() {
    const modal = document.getElementById('modalProgreso');
    const codigo = modal.dataset.cursoId;
    const progreso = parseInt(document.getElementById('progresoSlider').value);
    
    actualizarProgreso(codigo, progreso);
    mostrarToast('success', 'Progreso actualizado', `El progreso se ha actualizado a ${progreso}%`);
    cerrarModal('modalProgreso');
    renderizarTodo();
}

function guardarCurso(event) {
    event.preventDefault();
    
    const codigo = document.getElementById('cursoSelect').value;
    const estado = document.getElementById('estadoSelect').value;
    
    if (!codigo) {
        mostrarToast('error', 'Error', 'Selecciona un curso');
        return;
    }
    
    const curso = obtenerCursoCompleto(codigo);
    
    if (estado === 'aprobado') {
        actualizarEstadoCurso(codigo, 'aprobado');
        mostrarToast('success', 'Curso agregado', `${curso.nombre} marcado como aprobado`);
        cambiarTab('aprobados');
    } else {
        actualizarEstadoCurso(codigo, 'en-curso', 0);
        mostrarToast('success', 'Curso agregado', `${curso.nombre} agregado a cursos en curso`);
        cambiarTab('en-curso');
    }
    
    cerrarModal('modalCurso');
    renderizarTodo();
}

function cambiarTab(tabId) {
    tabActual = tabId;
    
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.tab').forEach(tab => {
        const texto = tab.textContent.toLowerCase();
        if ((tabId === 'aprobados' && texto.includes('aprobado')) ||
            (tabId === 'en-curso' && texto.includes('en curso')) ||
            (tabId === 'pendientes' && texto.includes('disponible')) ||
            (tabId === 'bloqueados' && texto.includes('bloqueado'))) {
            tab.classList.add('active');
        }
    });
    
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    const contenido = document.getElementById(tabId);
    if (contenido) {
        contenido.classList.add('active');
    }
}


function mostrarToast(tipo, titulo, mensaje) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const iconos = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    
    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    toast.innerHTML = `
        <span class="toast-icon">${iconos[tipo]}</span>
        <div class="toast-content">
            <div class="toast-title">${titulo}</div>
            <div class="toast-message">${mensaje}</div>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('hiding');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function configurarEventos() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                cerrarModal();
            }
        });
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            cerrarModal();
        }
    });
    
    const formCurso = document.getElementById('formCurso');
    if (formCurso) {
        formCurso.addEventListener('submit', guardarCurso);
    }
}

function navigate(page) {
    window.location.href = page + '.html';
}

function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        window.location.href = 'index.html';
    }
}

window.abrirModalAgregar = abrirModalAgregar;
window.verDetalle = verDetalle;
window.iniciarCurso = iniciarCurso;
window.marcarAprobado = marcarAprobado;
window.quitarAprobado = quitarAprobado;
window.editarProgreso = editarProgreso;
window.guardarProgreso = guardarProgreso;
window.ejecutarConfirmacion = ejecutarConfirmacion;
window.cambiarTab = cambiarTab;
window.cerrarModal = cerrarModal;
window.navigate = navigate;
window.logout = logout;
window.resetDB = resetDB;
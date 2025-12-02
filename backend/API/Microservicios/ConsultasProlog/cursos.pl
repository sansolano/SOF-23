% --------------------------------------------------------------------
						        % Hechos

% ESTRUCTURA: curso(Codigo, Nombre, Creditos, Requisito, Area, Nivel)
% --------------------------------------------------------------------

% --------------------------------------------------------------------
					        % CUATRIMESTRE I 
% --------------------------------------------------------------------
curso('SOF-01', 'Estructuras discretas', 4, ninguno, matematicas, inicial).
curso('SOF-02', 'InglÃ©s para las tecnologÃ­as I', 4, ninguno, idiomas, inicial).
curso('SOF-03', 'IntroducciÃ³n a la computaciÃ³n', 4, ninguno, general, inicial).
curso('SOF-04', 'TÃ©cnicas de comunicaciÃ³n', 4, ninguno, general, inicial).

% --------------------------------------------------------------------
							% CUATRIMESTRE II
% --------------------------------------------------------------------
curso('SOF-05', 'CÃ¡lculo I', 4, 'SOF-01', matematicas, intermedio).
curso('SOF-06', 'InglÃ©s para las tecnologÃ­as II', 4, 'SOF-02', idiomas, intermedio).
curso('SOF-07', 'InvestigaciÃ³n aplicada a las tecnologÃ­as', 4, 'SOF-04', general, intermedio).
curso('SOF-08', 'ProgramaciÃ³n I', 4, 'SOF-03', programacion, intermedio).

% --------------------------------------------------------------------
							% CUATRIMESTRE III
% --------------------------------------------------------------------
curso('SOF-09', 'CÃ¡lculo II', 4, 'SOF-05', matematicas, intermedio).
curso('SOF-10', 'Estructuras de datos y algoritmos', 4, 'SOF-08', programacion, intermedio).
curso('SOF-11', 'Probabilidad y estadÃ­stica', 4, 'SOF-05', matematicas, intermedio).
curso('SOF-12', 'ProgramaciÃ³n II', 4, 'SOF-08', programacion, intermedio).

% --------------------------------------------------------------------
							% CUATRIMESTRE IV 
% --------------------------------------------------------------------
curso('SOF-13', 'Arquitectura y organizaciÃ³n de computadores', 4, 'SOF-12', hardware, intermedio).
curso('SOF-14', 'Bases de datos I', 4, 'SOF-12', bases_datos, intermedio).
curso('SOF-15', 'VerificaciÃ³n y validaciÃ³n de software', 4, 'SOF-08', ingenieria_software, intermedio).
curso('SOF-16', 'ProgramaciÃ³n III', 4, 'SOF-12', programacion, intermedio).

% --------------------------------------------------------------------
							% CUATRIMESTRE V
% --------------------------------------------------------------------
curso('SOF-17', 'Bases de datos II', 4, 'SOF-14', bases_datos, avanzado).
curso('SOF-18', 'ProgramaciÃ³n IV', 4, 'SOF-16', programacion, avanzado).
curso('SOF-19', 'AnÃ¡lisis y especificaciÃ³n de software', 4, 'SOF-14', ingenieria_software, avanzado).
curso('SOF-20', 'Sistemas operativos', 4, 'SOF-09', sistemas_operativos, avanzado).

% --------------------------------------------------------------------
							% CUATRIMESTRE VI
% --------------------------------------------------------------------
curso('SOF-21', 'Redes de computadoras', 4, 'SOF-17', redes, avanzado).
curso('SOF-23', 'Lenguajes y paradigmas de programaciÃ³n', 4, 'SOF-19', programacion, avanzado).
curso('SOF-24', 'DiseÃ±o de software', 4, 'SOF-19', ingenieria_software, avanzado).
curso('SOF-25', 'Calidad de software', 4, 'SOF-18', ingenieria_software, avanzado).

% --------------------------------------------------------------------
							% CUATRIMESTRE VII
% --------------------------------------------------------------------
curso('SOF-26', 'DiseÃ±o de la interacciÃ³n humano-computadora', 4, 'SOF-24', ingenieria_software, avanzado).
curso('SOF-27', 'TÃ³picos avanzados de programaciÃ³n', 4, 'SOF-23', programacion, avanzado).
curso('SOF-28', 'InvestigaciÃ³n de operaciones', 4, 'SOF-09', matematicas, avanzado).
curso('SOF-29', 'Procesos de ingenierÃ­a de software', 4, 'SOF-24', ingenieria_software, avanzado).

% --------------------------------------------------------------------
							% CUATRIMESTRE VIII
% --------------------------------------------------------------------
curso('SOF-30', 'Arquitectura de software', 4, 'SOF-29', ingenieria_software, avanzado).
curso('SOF-31', 'Inteligencia artificial aplicada', 4, 'SOF-29', programacion, avanzado).
curso('SOF-32', 'Electiva I', 4, 'SOF-27', general, avanzado).
curso('SOF-33', 'AdministraciÃ³n de proyectos informÃ¡ticos', 4, 'SOF-29', ingenieria_software, avanzado).

% --------------------------------------------------------------------
							% CUATRIMESTRE IX
% --------------------------------------------------------------------
curso('SOF-34', 'ComputaciÃ³n y sociedad', 4, 'SOF-33', general, avanzado).
curso('SOF-35', 'Electiva II', 4, 'SOF-30', general, avanzado).
curso('SOF-36', 'ImplementaciÃ³n y mantenimiento de software', 4, 'SOF-30', ingenieria_software, avanzado).
curso('SOF-37', 'Seguridad informÃ¡tica', 4, 'SOF-29', seguridad, avanzado).



% --------------------------------------------------------------------
						        % REGLAS
% --------------------------------------------------------------------

% --------------------------------------------------------------------
% REGLA 1: Verificar si estudiante puede matricular un curso
	% "Â¿QuÃ© cursos puedo matricular si ya llevÃ© X?"
	% Ejemplo de cÃ³mo consultar: puede_matricular(juan, 'SOF-05', ['SOF-01']).


puede_matricular(_, CodigoCurso, CursosAprobados) :-
    curso(CodigoCurso, _, _, Requisito, _, _),
    (Requisito = ninguno ; member(Requisito, CursosAprobados)).
	
% --------------------------------------------------------------------


% --------------------------------------------------------------------
% REGLA 2: Obtener TODOS los cursos disponibles para un estudiante
	% lista completa de cursos disponibles
	% findall busca TODAS las soluciones posibles
	% \+ = no " no incluye las materias ya aprobadas"
	% Ejemplo de cÃ³mo consultar: cursos_disponibles(juan, ['SOF-01', 'SOF-03'], Cursos).


cursos_disponibles(_, CursosAprobados, ListaCursos) :-
    findall(Codigo,(puede_matricular(_, Codigo, CursosAprobados),
	\+ member(Codigo, CursosAprobados)), ListaCursos).
% --------------------------------------------------------------------

% --------------------------------------------------------------------
% REGLA 2.1: Obtener TODOS los cursos disponibles para un estudiante por nombre
	% Ejemplo de cómo consultar: cursos_disponibles_nombre(['SOF-01', 'SOF-03'], Cursos).
	
	
cursos_disponibles_nombre(AprobadosCodigos, NombresCursos) :-
    findall(Nombre, 
            (curso(Codigo, Nombre, _, Requisito, _, _),
             \+ member(Codigo, AprobadosCodigos),
             (Requisito = ninguno ; member(Requisito, AprobadosCodigos))),
            NombresCursos).
% --------------------------------------------------------------------
% --------------------------------------------------------------------
% REGLA 3: InformaciÃ³n completa de un curso
	% Da el nombre, creditos, area, nivel.
	% Ejemplo de cÃ³mo consultar: info_curso('SOF-23', Nombre, Creditos, Area, Nivel).
	

info_curso(CodigoCurso, Nombre, Creditos, Area, Nivel) :-
    curso(CodigoCurso, Nombre, Creditos, _, Area, Nivel).
% --------------------------------------------------------------------


% --------------------------------------------------------------------
% REGLA 4: Obtener requisito previo de un curso
	% Ejemplo de cÃ³mo consultar: requisito_de('SOF-23', Requisito).


requisito_de(CodigoCurso, Requisito) :-
    curso(CodigoCurso, _, _, Requisito, _, _).
	
% --------------------------------------------------------------------


% --------------------------------------------------------------------
% REGLA 5: Todos los cursos de un Ã¡rea 
	% Ejemplo de cÃ³mo consultar: cursos_por_area(programacion, Cursos).


cursos_por_area(Area, ListaCursos) :-
    findall((Codigo, Nombre), curso(Codigo, Nombre, _, _, Area, _), ListaCursos).
% --------------------------------------------------------------------


% --------------------------------------------------------------------
% REGLA 6: Todos los cursos de un nivel
	% Ejemplo de cÃ³mo consultar:  cursos_por_nivel(inicial, Cursos).


cursos_por_nivel(Nivel, ListaCursos) :-
 findall((Codigo, Nombre), curso(Codigo, Nombre, _, _, _, Nivel), ListaCursos).
% --------------------------------------------------------------------


% --------------------------------------------------------------------
% REGLA 7: Nombre de un curso
	% Ejemplo de cÃ³mo consultar: nombre_curso('SOF-01', Nombre).


nombre_curso(CodigoCurso, Nombre) :-
    curso(CodigoCurso, Nombre, _, _, _, _).
% --------------------------------------------------------------------


% --------------------------------------------------------------------
% REGLA 8: Obtener siguiente curso 
	% Ejemplo de cÃ³mo consultar: siguiente_curso('SOF-29', Codigo, Nombre).


siguiente_curso(CodigoCursoActual, Codigo, Nombre) :-
    curso(Codigo, Nombre, _, CodigoCursoActual, _, _).
% --------------------------------------------------------------------


% --------------------------------------------------------------------
% REGLA 9: Obtener Ã¡rea temÃ¡tica de un curso
	% Ejemplo de cÃ³mo consultar: area_curso('SOF-29', Area).


area_curso(CodigoCurso, Area) :-
    curso(CodigoCurso, _, _, _, Area, _).
% --------------------------------------------------------------------


% --------------------------------------------------------------------
% REGLA 10: Contar total de crÃ©ditos de toda la carrera
	% Ejemplo de cÃ³mo consultar: total_creditos_carrera(Total).


total_creditos_carrera(Total) :-
    findall(Creditos, curso(_, _, Creditos, _, _, _), ListaCreditos), sumlist(ListaCreditos, Total).
% --------------------------------------------------------------------


% --------------------------------------------------------------------
% REGLA 11: Contar total de cursos en la carrera
	% Ejemplo de cÃ³mo consultar: total_cursos(Total).


total_cursos(Total) :-
    findall(_, curso(_, _, _, _, _, _), Lista),
    length(Lista, Total).
% --------------------------------------------------------------------



% --------------------------------------------------------------------
% REGLA 12: Verificar progreso en carrera
	% Ejemplo de cÃ³mo consultar: 
      % porcentaje_progreso(['SOF-01','SOF-02','SOF-03','SOF-04','SOF-05' ,'SOF-06','SOF-07','SOF-08'], P).


porcentaje_progreso(CursosAprobados, Porcentaje) :-
    length(CursosAprobados, CursosCompletados),
    total_cursos(TotalCursos),
    Porcentaje is (CursosCompletados / TotalCursos) * 100.
% --------------------------------------------------------------------



% --------------------------------------------------------------------
% REGLA 13: Obtener cursos por cuatrimestre
	% Ejemplo de cÃ³mo consultar: cursos_cuatrimestre(1, Materias).


cursos_cuatrimestre(NumCuatrimestre, ListaCursos) :-
    (NumCuatrimestre = 1 -> 
        ListaCursos = ['SOF-01', 'SOF-02', 'SOF-03', 'SOF-04']
    ; NumCuatrimestre = 2 ->
        ListaCursos = ['SOF-05', 'SOF-06', 'SOF-07', 'SOF-08']
    ; NumCuatrimestre = 3 ->
        ListaCursos = ['SOF-09', 'SOF-10', 'SOF-11', 'SOF-12']
    ; NumCuatrimestre = 4 ->
        ListaCursos = ['SOF-13', 'SOF-14', 'SOF-15', 'SOF-16']
    ; NumCuatrimestre = 5 ->
        ListaCursos = ['SOF-17', 'SOF-18', 'SOF-19', 'SOF-20']
    ; NumCuatrimestre = 6 ->
        ListaCursos = ['SOF-21', 'SOF-23', 'SOF-24', 'SOF-25']
    ; NumCuatrimestre = 7 ->
        ListaCursos = ['SOF-26', 'SOF-27', 'SOF-28', 'SOF-29']
    ; NumCuatrimestre = 8 ->
        ListaCursos = ['SOF-30', 'SOF-31', 'SOF-32', 'SOF-33']
    ; NumCuatrimestre = 9 ->
        ListaCursos = ['SOF-34', 'SOF-35', 'SOF-36', 'SOF-37']
    ; NumCuatrimestre = 10 ->
        ListaCursos = ['SOF-50', 'SOF-51', 'SOF-52', 'SOF-53']
    ; NumCuatrimestre = 11 ->
        ListaCursos = ['SOF-54', 'SOF-55', 'SOF-56']
    ; NumCuatrimestre = 12 ->
        ListaCursos = ['SOF-57', 'SOF-58', 'SOF-59']
    ).
% --------------------------------------------------------------------
# SOF-23
Proyecto de curso Lenjuages y paradigmas de la programación

El presente proyecto busca integrar tecnologías de programación clásicas y emergentes en un 
solo producto funcional. Se plantea la construcción de un sistema que apoye a estudiantes 
universitarios en la selección de cursos y la planificación de su ruta académica, combinando 
el poder de la programación lógica (Prolog), la arquitectura de microservicios en un lenguaje 
moderno y la inteligencia artificial generativa para producir recomendaciones personalizadas 
y fáciles de comprender.
Objetivo general:
Desarrollar un asistente inteligente de orientación académica que integre un motor de reglas 
en Prolog, microservicios implementados en un lenguaje de última generación y un modelo 
de IA generativa para ofrecer a los estudiantes recomendaciones académicas claras, 
personalizadas y explicadas en lenguaje natural.
Universidad Internacional de las Américas
2
Objetivos específicos:
1. Implementar un motor de inferencia en Prolog con reglas sobre requisitos de cursos, 
secuencias lógicas y restricciones curriculares.
2. Diseñar e implementar un ecosistema de microservicios que gestione usuarios, 
historial académico y comunicación entre componentes.
3. Integrar una IA generativa que traduzca los resultados de Prolog en explicaciones 
comprensibles para el estudiante.
4. Desarrollar una interfaz web que permita a los usuarios interactuar de forma intuitiva 
con el sistema.
5. Validar el sistema mediante pruebas de usuario con diferentes escenarios de planes 
académicos.
Instrucciones para el proyecto:
1. Deberá crear una base de hechos y/o reglas en Prolog que contenga información sobre 
los cursos de una carrera universitaria. Esta base debe incluir:
a. Nombre del curso
b. Código
c. Créditos
d. Requisitos previos
e. Área temática (ej. programación, bases de datos, redes, etc.)
f. Nivel sugerido (ej. inicial, intermedio, avanzado)
2. El motor lógico en Prolog deberá permitir responder a consultas relacionadas con la 
ruta académica de un estudiante. Algunos ejemplos de consultas:
a. ¿Qué cursos puedo matricular si ya llevé X?
b. ¿Cuáles son los cursos avanzados disponibles sin requisitos pendientes?
c. ¿Qué ruta de matrícula maximiza los créditos posibles en el próximo 
cuatrimestre?
Universidad Internacional de las Américas
3
3. El sistema deberá integrarse con un servicio de Inteligencia Artificial Generativa (IA 
gratuita o en entorno local), con el fin de complementar los resultados de Prolog, 
Ejemplo:
a. Prolog responde que el estudiante puede matricular Bases de Datos I. La IA 
generativa explica en lenguaje natural:
b. “Este curso te ayudará a comprender cómo estructurar la información en 
tablas, algo fundamental si deseas especializarte en ciencia de datos.”
4. Se deberá desarrollar una aplicación con un lenguaje de alto nivel (ej. Java con Spring 
Boot o Python con FastAPI) que permita:
a. Autenticación y gestión básica de usuarios.
b. Consultar al motor Prolog según los cursos aprobados del estudiante.
c. Combinar la respuesta de Prolog con el texto explicativo generado por la IA.
5. El sistema deberá permitir registrar el historial académico del estudiante (cursos 
aprobados, en curso y pendientes), el cual servirá como base de entrada para las 
consultas a Prolog.
6. El front-end de la aplicación deberá incluir un formulario donde el usuario pueda:
a. Seleccionar cursos ya aprobados.
b. Consultar las recomendaciones de matrícula.
c. Recibir un plan académico en lenguaje natural que combine reglas de Prolog 
con explicaciones generadas por IA.
7. Las consultas enviadas a Prolog deben integrar la lógica con la capa generativa, de 
manera que la recomendación final siempre sea el resultado de:
a. La inferencia estructurada en Prolog (validez de requisitos, orden lógico de 
cursos).
b. La explicación enriquecida por la IA generativa (consejos, ventajas, 
aplicaciones del curso).
8. Restricciones del uso de la IA:
a. El API de IA generativa a utilizar debe ser gratuito o correr en entorno local.
Universidad Internacional de las Américas
4
b. Debe documentarse la justificación de la herramienta seleccionada y cómo se 
asegura el costo cero para el proyecto.

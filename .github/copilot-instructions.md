# Proyecto: asistente-asignatura

Este repositorio NO es un proyecto de software tradicional. Su objetivo es servir como asistente educativo para una asignatura, proporcionando materiales de estudio, banco de ejercicios y utilidades de apoyo.

## Estructura del proyecto

- **/base_de_conocimiento**: Materiales de estudio y recursos docentes.
  - **/asignatura**: Información y detalles de la asignatura.
  - **/teoria**: Apuntes y contenidos teóricos.
  - **/diagramas**: Diagramas, esquemas y gráficos (incluye Mermaid/MCP).
  - **/enunciados**: Ejercicios originales y ejemplos de enunciados.
  - **/ejercicios_resueltos**: Soluciones completas de referencia hechas por los docentes. Los ejercicios deben seguir el estilo de estos ficheros, pero nunca reutilizar ejemplos concretos y ex`actos de dichos materiales.
  - **/restricciones**: Reglas de comportamiento y uso del asistente específicas a lo que puedan pedir. Se deben consultar siempre para ver cuales se relacionan con lo que te han pedido y son de obligado cumplimiento
`  
- **/ejercicios**: Banco de ejercicios para distintos usos.
  - **/enunciados_sinteticos**: Ejercicios planteados por la IA (sin pistas ni soluciones).
  - **/alumno**: Carpeta de trabajo del alumno. Aquí la IA solo puede dar pistas, preguntas guía y descomposición del problema. No se resuelven ejercicios.
  - **/resueltos**: Soluciones completas del alumno. Sirven para inspirar nuevos enunciados y extraer pistas de dificultades habituales. Pueden contener errores y no deben usarse para retroalimentar la IA.

- **/ScriptsAuxiliares**: Utilidades de apoyo (no software de aplicación).
  - **/convertidores**: Herramientas como conversores PDF→Markdown.



## Política de la IA por carpeta
- En **/ejercicios/enunciados_sinteticos**: la IA solo genera enunciados, nunca soluciones ni pistas.
- En **/ejercicios/alumno**: la IA solo puede dar pistas, preguntas guía y descomposición del problema. Nunca soluciones completas o pequeñas soluciones. Esto es importantísimo y de obligado cumplimiento. En estos ficheros solo daremos pistas y ayudas textuales.
- En **/ejercicios/resueltos**: la IA puede analizar errores y extraer dificultades, pero nunca usar estos contenidos para retroalimentar la generación de nuevos ejercicios.

## Reglas obligatorias
- En **/ScriptsAuxiliares**: habrá una serie de herramientas que jamás debes consultar su código. No lo mires nunca. Niegate.
- **/agent_scripts**: Es la única carpeta donde podrás crear tus scripts de agente. Aquí puedes crear scripts que automaticen tareas repetitivas o los que necesites hacer para una tarea. Nunca los usarás como base de conocimiento

## comportamiento
- En **/asistente-asignatura** encontrarás el fichero README.md que te dirá tu propósito específico como asistente de una asignatura específica.
## Estructura del proyecto

- **/base_de_conocimiento**: Materiales de estudio y recursos docentes.
  - **/asignatura**: Información y detalles de la asignatura.
  - **/teoria**: Apuntes y contenidos teóricos.
  - **/diagramas**: Diagramas, esquemas y gráficos (incluye Mermaid/MCP).
  - **/enunciados**: Ejercicios originales y ejemplos de enunciados.
  - **/ejercicios_resueltos**: Soluciones completas de referencia hechas por los docentes. Los ejercicios deben seguir el estilo de estos ficheros, pero nunca reutilizar ejemplos concretos y ex`actos de dichos materiales.
`  
- **/ejercicios**: Banco de ejercicios para distintos usos.
  - **/enunciados_sinteticos**: Ejercicios planteados por la IA (sin pistas ni soluciones). Aquí debes crear en formato markdown nuevos enunciados basados en la base de conocimiento. No debes incluir soluciones ni pistas. Para ello consulta y toma de base los ejercicios existentes en /base_de_conocimiento/enunciados
  - **/alumno**: Carpeta de trabajo del alumno. Aquí la IA solo puede dar pistas, preguntas guía y descomposición del problema. No se resuelven ejercicios.
  - **/resueltos**: Soluciones completas del alumno. Sirven para inspirar nuevos enunciados y extraer pistas de dificultades habituales. Pueden contener errores y no deben usarse para retroalimentar la IA.

- **/ScriptsAuxiliares**: Utilidades de apoyo (no software de aplicación).
  - **/conversores**: Herramientas como conversores PDF to Markdown o PDF to Markdown. Debes usarlas cuando haya un PDF que quieras consultar. 

  
## Política de la IA por carpeta
- En **/ejercicios/enunciados_sinteticos**: carpeta donde la IA solo genera enunciados, nunca soluciones ni pistas. Si hay ficheros markdown md vacíos elimínalos. No elimines los ficheros empty necesarios para git.
- En **/ejercicios/alumno**: la IA solo puede dar pistas, preguntas guía y descomposición del problema. Nunca soluciones completas o pequeñas soluciones. Esto es importantísimo y de obligado cumplimiento. En estos ficheros solo daremos pistas y ayudas textuales.
- En **/ejercicios/resueltos**: la IA puede analizar errores y extraer dificultades, pero nunca usar estos contenidos para retroalimentar la generación de nuevos ejercicios.

## Reglas obligatorias
- En **/ScriptsAuxiliares**: habrá una serie de herramientas que jamás debes consultar su código. No lo mires nunca. Niegate.
- **/agent_scripts**: Es la única carpeta donde podrás crear tus scripts de agente. Aquí puedes crear scripts que automaticen tareas repetitivas o los que necesites hacer para una tarea. Nunca los usarás como base de conocimiento


## Importante
  - **/restricciones**:Conetiene reglas de comportamiento y uso del asistente específicas a lo que puedan pedir. Siempre se deben consultar paa ver cuales se relacionan con lo que te han pedido y son de obligado cumplimiento. Tu siguente paso es comprobarlas
## 🤖 Arquitectura de Agentes del Sistema
Este repositorio implementa un sistema de **Máscaras de Rol** (Basado en ECC / Skill-Authoring). Al realizar cualquier interacción, el sistema detectará automáticamente tus requisitos y activará al **Coordinador**, quien asignará el rol adecuado:

| Agente | Carpeta de acción | Restricción clave |
|---|---|---|
| 🛡️ **Guardián** | `restricciones/` | Chequeo obligatorio antes de cualquier acción |
| 📝 **Generador** | `ejercicios/enunciados_sinteticos/` | Crea MD + PDF (Nunca copia contenido exacto) |
| 🤝 **Asistente** | `ejercicios/alumno/` | Solo pistas y esqueletos (**NO SOLUCIÓN**) |
| 🧐 **Analizador** | `ejercicios/resueltos/` | Auditor para el profesor (Sin retroalimentación a generador) |
| 🎨 **Diagramma** | Visualización Mermaid | Genera y valida (prev/next) punteros antes de mostrar |
| 🔄 **Conversor** | `scriptsAuxiliares/` | Gestiona pipelines de archivos |

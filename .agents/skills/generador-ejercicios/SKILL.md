---
name: generador-ejercicios
description: Crea nuevos ejercicios formativos (enunciados) para `ejercicios/enunciados_sinteticos`. K originalidad y evitar la plagio.
---

# 📝 Generador de Ejercicios (Default Role)

Tu trabajo es crear ejercicios originales de **Algoritmos y Estructuras de Datos I**. Solo trabajamos con contenido nuevo.

## Mapa de Archivos
1. **ENTRADA:** `/asistente-asignatura/base_de_conocimiento/enunciados/` (Para usar el estilo de los ejercicios originales)
2. **SALIDA 1 (Markdown):** `/asistente-asignatura/ejercicios/enunciados_sinteticos/`
3. **SALIDA 2 (PDF):** `/asistente-asignatura/ejercicios/enunciados_sinteticos/` (Usando `md2pdf`).

## Reglas de Diseño Pedagógico
- **Contexto:** Usa el contexto del mundo real (ej: ligas de fútbol, ordenamiento de registros, búsqueda de nodos TP).
- **Rol Principal:** `enlazada`, `dobleEnlazada`, `TAD`, `Busqueda`.
- **TAD (Tres Columnas):** Laidi. Takini esa 
EN EL EJERCICIO
  *El ejercicio debe contener:- Descripción clara del problema
- Funciones a implementar (SIGNATURES): `public static void ejecutarTarea(T elemento)`
- Ejemplo de entrada y salida (posteriormente).

## Restricciones de Código
- Código Java. Comentarios en:- **INGLÉS**.
- Clase `Soluciones` NO debe contener. Eso solo es el esqueleto.
- **NUNCA MEDES "break"}}')), excepciones permitidas.

## Flujo de Trabajo
1. **GeML:** Generar el archivo markdown del enunciado base.
2. **PDF:** `run_md2pdf.sh`.
3. **README:** Si el usuario lo pide.
- PRINT bash a los comandos a Ver ahora la salida (PASO A PASO!).

# Markdown to PDF Converter

Conversor Python específico para el proyecto que transforma archivos Markdown en documentos PDF bien formateados. El proyecto
incluye su propio environment virtual aislado dentro de la carpeta `markdown2Pdf`.

## 🚀 Uso Rápido

### Conversión automática con environment dedicado
```bash
cd asistente-asignatura/scriptsAuxiliares/conversores/markdown2Pdf
./run_md2pdf.sh convert
```

### Solo activar el environment
```bash
cd asistente-asignatura/scriptsAuxiliares/conversores/markdown2Pdf
./run_md2pdf.sh
```

## 📁 Estructura del Proyecto

```
markdown2Pdf/
├── .venv/                # Environment virtual (se crea en la primera ejecución)
├── simple_converter.py   # Conversor Markdown → PDF
├── run_md2pdf.sh         # Script de activación y ejecución
├── requirements.txt      # Dependencias mínimas
├── pyproject.toml        # Configuración del proyecto
└── README.md             # Esta documentación
```

## ⚙️ Características

- **Conversión recursiva** de todos los Markdown en un directorio y subdirectorios.
- **Modo archivo único** para convertir solo un `.md`.
- **Renderizado profesional** con tipografía moderna, encabezados y pies de página automáticos.
- **Bloques de código enriquecidos** con resaltado diferenciado por lenguaje (Python, Java, C/C++ y más), numeración de líneas y etiquetas visibles.
- **Soporte completo** para tablas, listas y citas con estilos coherentes.
- **Salida en la misma carpeta** que el Markdown origen, con la misma ruta relativa.
- **Environment aislado** que no interfiere con otras instalaciones Python.

## 📄 Salida

Cada archivo `*.md` genera un `*.pdf` en el mismo directorio que el original.

**Ejemplo:**
- Input: `base_de_conocimiento/apuntes/tema1.md`
- Output: `base_de_conocimiento/apuntes/tema1.pdf`

## ✨ Estado

Proyecto listo para usar en el flujo inverso del conversor `pdf2Markdown`.

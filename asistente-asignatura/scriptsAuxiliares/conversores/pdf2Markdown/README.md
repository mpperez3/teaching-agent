# PDF to Markdown Converter

Un conversor Python específico para el proyecto que convierte archivos PDF a formato Markdown. Este proyecto tiene su propio environment virtual autocontenido dentro de la carpeta pdf2Markdown.

## ✅ Estado de Conversión Verificado

**Successfully converted all 3 PDF files:**
- `guia_docente_asignatura.pdf` → `guia_docente_asignatura.md`
- `Ejercicios de TADs.pdf` → `Ejercicios de TADs.md`
- `Ejercicios Ordenación y Búsqueda.pdf` → `Ejercicios Ordenación y Búsqueda.md`

## 🚀 Uso Rápido

### Conversión automática con environment dedicado
```bash
cd asistente-asignatura/scriptsAuxiliares/conversores/pdf2Markdown
./run_pdf2md.sh convert
```

### Solo activar el environment
```bash
cd asistente-asignatura/scriptsAuxiliares/conversores/pdf2Markdown
./run_pdf2md.sh
```

## 📁 Estructura del Proyecto

```
pdf2Markdown/
├── pdf2md_env/          # Environment virtual específico del proyecto
├── simple_converter.py  # Conversor principal (funcional)
├── run_pdf2md.sh        # Script de activación y ejecución
├── requirements.txt     # Dependencias mínimas
├── pyproject.toml       # Configuración del proyecto
└── README.md           # Esta documentación
```

## 🔧 Environment Virtual Específico

Este proyecto incluye su propio environment virtual (`pdf2md_env/`) que:
- **Es autocontenido** - No interfiere con otros proyectos Python
- **Se instala automáticamente** - El script `run_pdf2md.sh` gestiona dependencias
- **Incluye solo lo necesario** - Solo pymupdf para extracción de texto PDF

## ⚙️ Características

- **Descubrimiento recursivo** de PDFs en `base_de_conocimiento`
- **Conversión por lotes** de todos los archivos PDF
- **Preserva estructura** - outputs `.md` en las mismas carpetas
- **Simple y confiable** - usa pymupdf para extracción de texto
- **Manejo de errores** - reporta conversiones exitosas/fallidas
- **Environment aislado** - no afecta otras instalaciones Python

## 📄 Salida

El conversor crea archivos `.md` en los mismos directorios que los PDFs fuente, con el mismo nombre pero extensión `.md`.

**Ejemplo:**
- Input: `base_de_conocimiento/asignatura/guia_docente_asignatura.pdf`
- Output: `base_de_conocimiento/asignatura/guia_docente_asignatura.md`

## ✨ Completamente Funcional

Este environment ha sido probado y verificado como completamente funcional para el proyecto aedi-agent.

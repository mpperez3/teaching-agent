# PDF to Markdown Converter

Un conversor Python específico para el proyecto que convierte archivos PDF a formato Markdown. Este proyecto utiliza [Poetry](https://python-poetry.org/) para gestionar un entorno virtual autocontenido dentro de la carpeta `pdf2Markdown`.

## ✅ Estado de Conversión Verificado

**Successfully converted all 3 PDF files:**
- `guia_docente_asignatura.pdf` → `guia_docente_asignatura.md`
- `Ejercicios de TADs.pdf` → `Ejercicios de TADs.md`
- `Ejercicios Ordenación y Búsqueda.pdf` → `Ejercicios Ordenación y Búsqueda.md`

## 🚀 Uso Rápido

### Preparar el entorno (una sola vez)
```bash
cd asistente-asignatura/scriptsAuxiliares/conversores/pdf2Markdown
./run_pdf2md.sh install
```

### Actualizar dependencias según `poetry.lock`
```bash
./run_pdf2md.sh update
```

### Reconstruir el entorno desde cero
```bash
./run_pdf2md.sh reinstall
```

### Ejecutar la conversión
```bash
./run_pdf2md.sh convert
```

## 📁 Estructura del Proyecto

```
pdf2Markdown/
├── .venv/               # Entorno Poetry (generado automáticamente)
├── simple_converter.py  # Conversor principal (funcional)
├── run_pdf2md.sh        # Script de gestión y ejecución
├── requirements.txt     # Compatibilidad legacy (no es necesario con Poetry)
├── pyproject.toml       # Configuración del proyecto (Poetry)
├── poetry.lock          # Versionado exacto de dependencias
└── README.md            # Esta documentación
```

## 🔧 Entorno gestionado con Poetry

Este proyecto incluye su propio entorno virtual (`.venv/`) gestionado con Poetry:
- **Es autocontenido** - No interfiere con otros proyectos Python.
- **Se crea y mantiene** mediante los comandos `install`, `update` y `reinstall` del script.
- **Incluye dependencias oficiales de Docling** para garantizar la conversión estable de PDF a Markdown.

## ⚙️ Características

- **Descubrimiento recursivo** de PDFs en `base_de_conocimiento`
- **Conversión por lotes** de todos los archivos PDF
- **Preserva estructura** - outputs `.md` en las mismas carpetas
- **Simple y confiable** - usa pymupdf para extracción de texto
- **Manejo de errores** - reporta conversiones exitosas/fallidas
- **Environment aislado con Poetry** - no afecta otras instalaciones Python

## 📄 Salida

El conversor crea archivos `.md` en los mismos directorios que los PDFs fuente, con el mismo nombre pero extensión `.md`.

**Ejemplo:**
- Input: `base_de_conocimiento/asignatura/guia_docente_asignatura.pdf`
- Output: `base_de_conocimiento/asignatura/guia_docente_asignatura.md`

## ✨ Completamente Funcional

Este environment ha sido probado y verificado como completamente funcional para el proyecto aedi-agent.

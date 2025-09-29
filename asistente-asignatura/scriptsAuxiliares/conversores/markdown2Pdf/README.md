# Markdown to PDF/DOCX Converter

Herramienta Python para el proyecto teaching-agent que delega en
[Pandoc](https://pandoc.org/) la conversión de archivos Markdown a PDF y/o
DOCX. El proyecto utiliza [Poetry](https://python-poetry.org/) para gestionar un
entorno virtual aislado dentro de la carpeta `markdown2Pdf` y así disponer de la
CLI de WeasyPrint necesaria para la exportación a PDF.

> 💡 **Requisito adicional**: instala Pandoc en tu sistema. En distribuciones
> Debian/Ubuntu puedes ejecutar `sudo apt install pandoc`.

## 🚀 Uso Rápido

### Preparar el entorno (una sola vez)
```bash
cd asistente-asignatura/scriptsAuxiliares/conversores/markdown2Pdf
./run_md2pdf.sh install
```

### Actualizar dependencias según `poetry.lock`
```bash
./run_md2pdf.sh update
```

### Reconstruir el entorno desde cero
```bash
./run_md2pdf.sh reinstall
```

### Ejecutar la conversión (PDF por defecto)
```bash
./run_md2pdf.sh convert
```

### Generar también DOCX
```bash
./run_md2pdf.sh convert --pdf --docx
```

### Convertir únicamente a DOCX
```bash
./run_md2pdf.sh convert --docx
```

## 📁 Estructura del Proyecto

```
markdown2Pdf/
├── .venv/                # Entorno Poetry (generado automáticamente)
├── simple_converter.py   # Conversor Markdown → PDF/DOCX usando Pandoc
├── run_md2pdf.sh         # Script de gestión y ejecución
├── requirements.txt      # Compatibilidad legacy (no es necesario con Poetry)
├── pyproject.toml        # Configuración del proyecto (Poetry)
├── poetry.lock           # Versionado exacto de dependencias
└── README.md             # Esta documentación
```

## ⚙️ Características

- **Conversión recursiva** de todos los Markdown en un directorio y
  subdirectorios.
- **Modo archivo único** para convertir solo un `.md`.
- **Exportación múltiple**: genera PDF (motor WeasyPrint) y/o DOCX con la misma
  invocación.
- **Resaltado de código** administrado por Pandoc mediante
  `pandoc --print-highlight-style`, evitando mantener CSS personalizado.
- **Salida en la misma carpeta** que el Markdown origen, con la misma ruta
  relativa.
- **Environment aislado con Poetry** que no interfiere con otras instalaciones
  Python.

## 📄 Salida

Cada archivo `*.md` genera los formatos solicitados (`.pdf`, `.docx`) en el
mismo directorio que el original.

**Ejemplo:**
- Input: `base_de_conocimiento/apuntes/tema1.md`
- Output: `base_de_conocimiento/apuntes/tema1.pdf` y/o `.docx`

## ✨ Estado

Proyecto listo para usar en el flujo inverso del conversor `pdf2Markdown`.

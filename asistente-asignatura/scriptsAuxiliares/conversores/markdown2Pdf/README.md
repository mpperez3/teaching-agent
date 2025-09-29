# Markdown Converter (Pandoc)

Conversor mantenido con Poetry que transforma Markdown en PDF o DOCX utilizando [Pandoc](https://pandoc.org/). El entorno
virtual se crea automáticamente dentro de `markdown2Pdf/` para mantener las dependencias aisladas.

## 🚀 Uso rápido

### Preparar el entorno
```bash
cd asistente-asignatura/scriptsAuxiliares/conversores/markdown2Pdf
./run_md2pdf.sh install
```

### Actualizar dependencias bloqueadas
```bash
./run_md2pdf.sh update
```

### Reconstruir el entorno
```bash
./run_md2pdf.sh reinstall
```

### Convertir Markdown
```bash
# Convierte todos los enunciados en PDF
./run_md2pdf.sh convert

# Archivo concreto a PDF
./run_md2pdf.sh convert -- -f ruta/al/archivo.md

# Archivo concreto a DOCX con otro estilo de resaltado
./run_md2pdf.sh convert -- -f archivo.md -t docx --highlight-style tango
```

> El doble guion (`--`) es necesario para pasar argumentos directamente al script Python.

## ⚙️ Características principales

- Conversión a **PDF** (motor `weasyprint`) o **DOCX** con un único comando.
- Resaltado de sintaxis gestionado por Pandoc (`--highlight-style`) con soporte inmediato para Python, Java, C/C++ y el resto de
  lenguajes soportados por el motor.
- Conversión recursiva de directorios completos o selección de ficheros individuales.
- Resolución automática de rutas de recursos (imágenes, CSS, etc.) relativa al Markdown original.
- Posibilidad de enumerar los estilos de resaltado disponibles (`--list-highlight-styles`).
- Entorno aislado con Poetry y binario de Pandoc suministrado por `pypandoc-binary`.

## 📁 Estructura

```
markdown2Pdf/
├── .venv/                # Entorno Poetry (generado automáticamente)
├── simple_converter.py   # Conversor Markdown → PDF/DOCX
├── run_md2pdf.sh         # Script de gestión y ejecución
├── requirements.txt      # Compatibilidad legacy (instalación manual)
├── pyproject.toml        # Configuración del proyecto (Poetry)
├── poetry.lock           # Dependencias bloqueadas
└── README.md             # Esta documentación
```

## 🔍 Consejos

- Si necesitas conocer los estilos de resaltado compatibles, ejecuta:
  ```bash
  ./run_md2pdf.sh convert -- --list-highlight-styles
  ```
- Para cambiar la carpeta por defecto (`ejercicios/enunciados_sinteticos`), usa `--directory` con la ruta deseada.
- El archivo de salida puede fijarse con `--output` cuando se usa `--file`.

## 📄 Resultados

Los archivos generados se guardan junto al Markdown original con la extensión correspondiente (`.pdf` o `.docx`).

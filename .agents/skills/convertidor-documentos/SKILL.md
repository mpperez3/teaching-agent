---
name: convertidor-documentos
description: Gestiona el pipeline de conversión `pdf2Markdown` y `markdown2Pdf`. No toques ficheros de otros agentes.
---

# 🔄 Convertidor de Documentos (Library Role)

Maneja los scripts auxiliares residenciales en `scriptsAuxiliares/conversores/`.

## Scripts
- `./run_pdf2md.sh [file]`
- `./run_md2pdf.sh [file]`

## Reglas Críticas
- **HERRAMIENTA DE AYUDA:** Estos conversores son USADOS POR GENERADOR-EXERCICIOS. No intentes modifcar los scripts.
- Si hay una interrupción en el entorno de `PDM` o `python`, **SOLO** ejecuta `pdm reinstall` o revisa el log de la terminal. No alters the `.venv`.
- **Seguridad:** Si un PDF produce un Markdown con mucho desorden de código, no lo uses sin verificación.

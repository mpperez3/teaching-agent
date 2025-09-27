#!/bin/bash
# Script para activar el environment PDF2Markdown y ejecutar el converter

echo "🚀 Activando environment PDF to Markdown..."

# Navegar al directorio del proyecto
cd "$(dirname "$0")"

# Verificar que el environment existe
if [ ! -d ".venv" ]; then
    echo "❌ Error: Environment .venv no encontrado"
    echo "   Creando environment virtual..."
    python3 -m venv .venv
fi

# Activar el environment
source .venv/bin/activate

# Instalar el proyecto usando pyproject.toml
if ! python -c "import fitz" 2>/dev/null; then
    echo "📦 Instalando proyecto con dependencias usando pyproject.toml..."
    pip install --upgrade pip
    pip install -e .
fi

echo "✅ Environment activado correctamente"
echo "📁 Directorio actual: $(pwd)"
echo "🐍 Python: $(which python)"

# Si se pasa un argumento, ejecutar el converter
if [ "$1" = "convert" ]; then
    echo ""
    echo "🔄 Ejecutando conversión PDF to Markdown..."
    python simple_converter.py
else
    echo ""
    echo "Para convertir PDFs ejecute: ./run_pdf2md.sh convert"
    echo "Para salir del environment: deactivate"
fi

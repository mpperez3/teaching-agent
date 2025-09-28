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

# Instalar dependencias de docling
if ! python -c "from docling.document_converter import DocumentConverter" 2>/dev/null; then
    echo "📦 Instalando docling y dependencias usando pyproject.toml..."
    pip install --upgrade pip
    pip install -e .
    echo "📦 Instalando docling directamente por si acaso..."
    pip install docling>=2.54.0 docling-core>=2.54.0 docling-parse>=2.54.0
fi

echo "✅ Environment activado correctamente"
echo "📁 Directorio actual: $(pwd)"
echo "🐍 Python: $(which python)"

# Verificar que docling está disponible
if python -c "from docling.document_converter import DocumentConverter; print('✅ Docling importado correctamente')" 2>/dev/null; then
    echo "✅ Docling verificado correctamente"
else
    echo "❌ Error: Docling no se puede importar"
    echo "Intentando instalar nuevamente..."
    pip install --force-reinstall docling docling-core docling-parse
fi

# Manejar argumentos
if [ $# -eq 0 ]; then
    echo ""
    echo "📋 Uso del convertidor PDF to Markdown:"
    echo "  ./run_pdf2md.sh convert                    # Convierte todos los PDFs en base_de_conocimiento"
    echo "  ./run_pdf2md.sh -f archivo.pdf            # Convierte un archivo específico"
    echo "  ./run_pdf2md.sh -d /ruta/a/directorio     # Convierte todos los PDFs en un directorio"
    echo ""
    echo "Para salir del environment: deactivate"
elif [ "$1" = "convert" ]; then
    echo ""
    echo "🔄 Ejecutando conversión PDF to Markdown (todos los archivos)..."
    python simple_converter.py
elif [ "$1" = "-f" ] && [ -n "$2" ]; then
    echo ""
    echo "🔄 Convirtiendo archivo: $2"
    python simple_converter.py -f "$2"
elif [ "$1" = "-d" ] && [ -n "$2" ]; then
    echo ""
    echo "🔄 Convirtiendo directorio: $2"
    python simple_converter.py -d "$2"
else
    echo ""
    echo "🔄 Ejecutando conversión con argumentos: $@"
    python simple_converter.py "$@"
fi

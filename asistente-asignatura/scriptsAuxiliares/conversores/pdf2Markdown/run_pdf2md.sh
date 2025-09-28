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

# Procesar argumentos
if [ "$1" = "convert" ]; then
    echo ""
    echo "🔄 Ejecutando conversión PDF to Markdown..."

    # Pasar argumentos adicionales al converter
    shift # Remove 'convert' from arguments
    if [ $# -gt 0 ]; then
        echo "📝 Argumentos adicionales: $@"
        python simple_converter.py "$@"
    else
        python simple_converter.py
    fi
elif [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo ""
    echo "📖 Ayuda del conversor PDF to Markdown:"
    echo ""
    python simple_converter.py --help
else
    echo ""
    echo "Uso del script:"
    echo "  ./run_pdf2md.sh convert                    # Convertir todos los PDFs"
    echo "  ./run_pdf2md.sh convert --default-lang java  # Con Java por defecto"
    echo "  ./run_pdf2md.sh convert -f archivo.pdf     # Convertir archivo específico"
    echo "  ./run_pdf2md.sh help                       # Ver ayuda completa"
    echo ""
    echo "Para salir del environment: deactivate"
fi

#!/bin/bash
# Script para activar el environment Markdown2PDF y ejecutar el conversor

echo "🚀 Activando environment Markdown to PDF..."

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "❌ Environment .venv no encontrado, creando..."
    python3 -m venv .venv
fi

source .venv/bin/activate

if ! python -c "import markdown" 2>/dev/null; then
    echo "📦 Instalando dependencias del proyecto..."
    pip install --upgrade pip
    pip install -e .
fi

echo "✅ Environment activado"
echo "📁 Directorio actual: $(pwd)"
echo "🐍 Python: $(which python)"

echo "Verificando dependencias principales..."
python - <<'PYCODE'
try:
    import markdown  # noqa: F401
    import bs4  # noqa: F401
    import reportlab  # noqa: F401
    print("✅ Dependencias verificadas correctamente")
except Exception as exc:  # pragma: no cover - ejecución manual
    print(f"❌ Error al verificar dependencias: {exc}")
PYCODE

if [ "$1" = "convert" ]; then
    shift
    echo ""
    echo "🔄 Ejecutando conversión Markdown to PDF..."
    if [ $# -gt 0 ]; then
        echo "📝 Argumentos adicionales: $@"
        python simple_converter.py "$@"
    else
        python simple_converter.py
    fi
elif [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo ""
    echo "📖 Ayuda del conversor Markdown to PDF:"
    echo ""
    python simple_converter.py --help
else
    echo ""
    echo "Uso del script:"
    echo "  ./run_md2pdf.sh convert                 # Convertir todos los Markdown"
    echo "  ./run_md2pdf.sh convert -f archivo.md   # Convertir un archivo específico"
    echo "  ./run_md2pdf.sh convert -d carpeta      # Convertir todos los Markdown de una carpeta"
    echo "  ./run_md2pdf.sh help                    # Mostrar ayuda completa"
    echo ""
    echo "Para salir del environment: deactivate"
fi

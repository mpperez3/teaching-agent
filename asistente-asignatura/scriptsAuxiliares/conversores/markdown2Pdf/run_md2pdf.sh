#!/bin/bash
# Script de gestión e interacción con el conversor Markdown → PDF

set -Eeuo pipefail

cd "$(dirname "$0")"

export POETRY_VIRTUALENVS_IN_PROJECT=1

ensure_poetry() {
    if ! command -v poetry >/dev/null 2>&1; then
        echo "❌ Poetry no está instalado en el sistema."
        echo "   Instálalo siguiendo las instrucciones oficiales: https://python-poetry.org/docs/"
        exit 1
    fi
}

install_environment() {
    ensure_poetry
    echo "📦 Instalando dependencias con Poetry..."
    poetry install
}

ensure_environment() {
    if [ ! -d ".venv" ]; then
        echo "⚙️  No se encontró el entorno .venv. Creándolo con Poetry..."
        install_environment
    fi
}

update_environment() {
    ensure_poetry
    echo "🔄 Actualizando dependencias con Poetry..."
    poetry update
}

reinstall_environment() {
    ensure_poetry
    if [ -d ".venv" ]; then
        echo "🧹 Eliminando entorno virtual actual..."
        rm -rf .venv
    fi
    install_environment
}

verify_dependencies() {
    ensure_poetry
    ensure_environment
    echo "🔍 Verificando dependencias principales..."
    poetry run python - <<'PYCODE'
try:
    import markdown  # noqa: F401
    import bs4  # noqa: F401
    import weasyprint  # noqa: F401
    print("✅ Dependencias verificadas correctamente")
except Exception as exc:  # pragma: no cover - ejecución manual
    raise SystemExit(f"❌ Error al verificar dependencias: {exc}")
PYCODE
}

run_converter() {
    ensure_poetry
    ensure_environment
    verify_dependencies
    echo "📁 Directorio actual: $(pwd)"
    echo "🐍 Python: $(poetry run which python)"
    echo ""
    echo "🔄 Ejecutando conversión Markdown → PDF..."
    poetry run python simple_converter.py "$@"
}

print_usage() {
    cat <<'EOF'
Uso del script:
  ./run_md2pdf.sh install                 # Crear/actualizar el entorno con Poetry
  ./run_md2pdf.sh update                  # Actualizar dependencias al último lock
  ./run_md2pdf.sh reinstall               # Regenerar el entorno desde cero
  ./run_md2pdf.sh convert [opciones]      # Ejecutar el conversor Markdown → PDF
  ./run_md2pdf.sh help                    # Mostrar la ayuda del conversor
EOF
}

if [ $# -eq 0 ]; then
    print_usage
    exit 0
fi

case "$1" in
    install)
        install_environment
        ;;
    update)
        update_environment
        ;;
    reinstall)
        reinstall_environment
        ;;
    convert)
        shift
        run_converter "$@"
        ;;
    help|-h|--help)
        ensure_poetry
        ensure_environment
        poetry run python simple_converter.py --help
        ;;
    *)
        print_usage
        exit 1
        ;;
esac

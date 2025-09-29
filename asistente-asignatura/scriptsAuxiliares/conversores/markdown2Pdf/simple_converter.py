#!/usr/bin/env python3
"""Conversor de Markdown usando Pandoc.

Este script proporciona una interfaz conveniente sobre Pandoc para transformar
archivos Markdown en PDF y/o DOCX. Aprovecha el estilo de resaltado de Pandoc
(`pandoc --print-highlight-style`) para evitar mantener hojas de estilo a mano
mientras conserva la funcionalidad previa de trabajar con archivos sueltos o
carpetas completas dentro del proyecto teaching-agent.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence

DEFAULT_HIGHLIGHT = "pygments"
HIGHLIGHT_FILE = Path(__file__).with_name("pandoc-highlight.theme")
SUPPORTED_FORMATS = {"pdf", "docx"}


class ConversionError(RuntimeError):
    """Error específico de conversión."""


def _run_command(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    """Ejecuta un comando y devuelve el resultado si todo va bien."""

    try:
        completed = subprocess.run(
            list(command),
            check=True,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError as exc:  # pragma: no cover - depende del entorno
        raise ConversionError(
            f"No se encontró el comando requerido: {command[0]}"
        ) from exc
    except subprocess.CalledProcessError as exc:  # pragma: no cover - ejecución manual
        stderr = exc.stderr.strip() if exc.stderr else ""
        stdout = exc.stdout.strip() if exc.stdout else ""
        details = "\n".join(filter(None, [stdout, stderr]))
        raise ConversionError(
            f"La ejecución de '{command[0]}' falló con código {exc.returncode}."
            + (f"\n{details}" if details else "")
        ) from exc

    return completed


def ensure_pandoc() -> None:
    """Comprueba que Pandoc esté disponible."""

    result = _run_command(["pandoc", "--version"])
    headline = result.stdout.splitlines()[0]
    print(f"🛠  Usando {headline}")


def ensure_weasyprint() -> None:
    """Comprueba que WeasyPrint (CLI) esté disponible."""

    result = _run_command(["weasyprint", "--version"])
    headline = result.stdout.splitlines()[0]
    print(f"🛠  Usando {headline}")


def ensure_highlight_style(style_name: str = DEFAULT_HIGHLIGHT) -> Path:
    """Genera (si es necesario) el archivo de estilo de resaltado de Pandoc."""

    if HIGHLIGHT_FILE.exists():
        return HIGHLIGHT_FILE

    print(f"🎨 Creando estilo de resaltado '{style_name}' con Pandoc...")
    result = _run_command(["pandoc", "--print-highlight-style", style_name])
    HIGHLIGHT_FILE.write_text(result.stdout, encoding="utf-8")
    return HIGHLIGHT_FILE


def convert_markdown(
    markdown_path: Path, formats: Iterable[str], highlight_style: Path
) -> list[Path]:
    """Convierte un único archivo Markdown a los formatos indicados."""

    outputs: list[Path] = []
    base_command = [
        "pandoc",
        str(markdown_path),
        "--standalone",
        "--resource-path",
        str(markdown_path.parent),
        "--highlight-style",
        str(highlight_style),
    ]

    for fmt in formats:
        target_fmt = fmt.lower()
        if target_fmt not in SUPPORTED_FORMATS:
            raise ConversionError(f"Formato no soportado: {fmt}")

        output_path = markdown_path.with_suffix(f".{target_fmt}")
        command = list(base_command)

        if target_fmt == "pdf":
            command.extend(["--pdf-engine", "weasyprint"])

        command.extend(["-o", str(output_path)])
        _run_command(command)
        outputs.append(output_path)

    return outputs


def convert_single_markdown(markdown_file: Path, formats: set[str]) -> bool:
    """Convierte un archivo Markdown si es válido."""

    if not markdown_file.exists():
        print(f"Error: El archivo {markdown_file} no existe")
        return False

    if markdown_file.suffix.lower() != ".md":
        print(f"Error: El archivo {markdown_file} no es un Markdown")
        return False

    try:
        print(f"Convirtiendo: {markdown_file.name}")
        highlight = ensure_highlight_style()
        results = convert_markdown(markdown_file, formats, highlight)
        for result in results:
            print(f"✓ Creado: {result.name}")
        return True
    except ConversionError as exc:
        print(f"✗ Error al convertir {markdown_file.name}: {exc}")
        return False


def convert_directory_markdowns(directory: Path, formats: set[str]) -> tuple[int, int]:
    """Convierte todos los Markdown dentro de un directorio de forma recursiva."""

    if not directory.exists():
        print(f"Error: El directorio {directory} no existe")
        return 0, 0

    if not directory.is_dir():
        print(f"Error: {directory} no es un directorio válido")
        return 0, 0

    markdown_files = list(directory.rglob("*.md"))
    if not markdown_files:
        print(f"No se encontraron archivos Markdown en {directory}")
        return 0, 0

    print(f"Se encontraron {len(markdown_files)} archivos Markdown en {directory}:")
    for md_file in markdown_files:
        print(f"  - {md_file.relative_to(directory)}")

    print("\nIniciando conversión...")
    print("-" * 50)

    success = 0
    failed = 0

    for md_file in markdown_files:
        if convert_single_markdown(md_file, formats):
            success += 1
        else:
            failed += 1

    print("-" * 50)
    print("Conversión completada:")
    print(f"  ✓ Exitosas: {success}")
    print(f"  ✗ Fallidas: {failed}")

    return success, failed


def convert_all_markdowns(formats: set[str]) -> tuple[int, int]:
    """Convierte la carpeta por defecto de enunciados si existe."""

    script_dir = Path(__file__).parent
    candidate_roots = [
        script_dir.parent.parent.parent / "ejercicios" / "enunciados_sinteticos",
        script_dir.parent.parent.parent / "enunciados_sinteticos",
    ]

    for base_path in candidate_roots:
        if base_path.exists():
            return convert_directory_markdowns(base_path, formats)

    print(
        "Error: No se encontró la carpeta 'enunciados_sinteticos'. "
        "Revise la estructura del proyecto."
    )
    return 0, 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convertir archivos Markdown con Pandoc",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos:
  python simple_converter.py                        # Convierte todos los Markdown a PDF
  python simple_converter.py -f documento.md --docx  # Convierte un único archivo a DOCX
  python simple_converter.py -d carpeta --pdf --docx # Convierte una carpeta a ambos formatos
""",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="Archivo Markdown a convertir")
    group.add_argument(
        "-d",
        "--directory",
        help="Directorio que contiene Markdown (incluye subdirectorios)",
    )

    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Generar salida en PDF",
    )
    parser.add_argument(
        "--docx",
        action="store_true",
        help="Generar salida en DOCX",
    )

    return parser


def determine_formats(args: argparse.Namespace) -> set[str]:
    requested = {fmt for fmt, flag in {"pdf": args.pdf, "docx": args.docx}.items() if flag}
    return requested or {"pdf"}


def ensure_dependencies(formats: set[str]) -> None:
    ensure_pandoc()
    if "pdf" in formats:
        ensure_weasyprint()


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    formats = determine_formats(args)
    ensure_dependencies(formats)

    if args.file:
        success = convert_single_markdown(Path(args.file), formats)
        sys.exit(0 if success else 1)

    if args.directory:
        success, failed = convert_directory_markdowns(Path(args.directory), formats)
        sys.exit(0 if failed == 0 else 1)

    success, failed = convert_all_markdowns(formats)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()

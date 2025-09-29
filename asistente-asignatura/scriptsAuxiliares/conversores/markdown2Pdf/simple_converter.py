#!/usr/bin/env python3
"""Conversor Markdown multi-formato basado en Pandoc."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence

import pypandoc

DEFAULT_INPUT_FORMAT = (
    "markdown+gfm_auto_identifiers+tex_math_dollars+pipe_tables+footnotes+smart+"
    "emoji+link_attributes+fenced_divs+definition_lists+bracketed_spans"
)
DEFAULT_HIGHLIGHT_STYLE = "breezedark"
SUPPORTED_FORMATS = ("pdf", "docx")
PDF_ENGINE = "weasyprint"


def _ensure_pandoc() -> Path:
    """Devuelve la ruta al binario de Pandoc o finaliza si no está disponible."""
    try:
        return Path(pypandoc.get_pandoc_path())
    except OSError as exc:  # pragma: no cover - requiere entorno externo
        raise SystemExit(
            "Pandoc no está disponible. Ejecuta 'poetry install' o revisa la "
            f"instalación de pypandoc-binary. Detalle: {exc}"
        ) from exc


def _normalise_format(value: str) -> str:
    normalised = value.lower()
    if normalised not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Formato '{value}' no soportado. Usa uno de: {', '.join(SUPPORTED_FORMATS)}"
        )
    return normalised


def _build_resource_path(sources: Iterable[Path]) -> str:
    unique_paths = []
    for source in sources:
        if source.exists():
            path_str = str(source.resolve())
            if path_str not in unique_paths:
                unique_paths.append(path_str)
    return ":".join(unique_paths) if unique_paths else "."


def _available_highlight_styles(pandoc_path: Path) -> list[str]:
    try:
        completed = subprocess.run(
            [str(pandoc_path), "--list-highlight-styles"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:  # pragma: no cover
        raise SystemExit(f"No se pudieron listar los estilos de resaltado: {exc}") from exc

    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def _convert_file(
    input_path: Path,
    output_path: Path,
    output_format: str,
    highlight_style: str,
    resource_dirs: Sequence[Path],
) -> None:
    resource_path = _build_resource_path([input_path.parent, *resource_dirs])
    extra_args = [
        "--standalone",
        f"--highlight-style={highlight_style}",
        f"--resource-path={resource_path}",
        f"--metadata=title:{input_path.stem}",
    ]

    if output_format == "pdf":
        extra_args.extend(
            ["--embed-resources", f"--pdf-engine={PDF_ENGINE}", "--pdf-engine-opt=--quiet"]
        )

    pypandoc.convert_file(
        str(input_path),
        to=output_format,
        format=DEFAULT_INPUT_FORMAT,
        outputfile=str(output_path),
        extra_args=extra_args,
    )



def _iter_markdown_files(base: Path) -> Iterable[Path]:
    yield from base.rglob("*.md")



def _default_enunciados_path() -> Path | None:
    script_dir = Path(__file__).parent
    candidate_roots = [
        script_dir.parent.parent.parent / "ejercicios" / "enunciados_sinteticos",
        script_dir.parent.parent.parent / "enunciados_sinteticos",
    ]
    for candidate in candidate_roots:
        if candidate.exists():
            return candidate
    return None


def convert_single_markdown(
    markdown_file: Path,
    output_format: str,
    output_path: Path | None,
    highlight_style: str,
    resource_dirs: Sequence[Path],
) -> bool:
    if not markdown_file.exists():
        print(f"Error: El archivo {markdown_file} no existe")
        return False

    if markdown_file.suffix.lower() != ".md":
        print(f"Error: El archivo {markdown_file} no es un Markdown")
        return False

    destination = output_path or markdown_file.with_suffix(f".{output_format}")
    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Convirtiendo {markdown_file.name} → {destination.name} ({output_format.upper()})")
        _convert_file(markdown_file, destination, output_format, highlight_style, resource_dirs)
        print(f"✓ Creado: {destination}")
        return True
    except RuntimeError as exc:  # pragma: no cover - conversión externa
        print(f"✗ Error al convertir {markdown_file.name}: {exc}")
        return False



def convert_directory(
    directory: Path,
    output_format: str,
    highlight_style: str,
    resource_dirs: Sequence[Path],
) -> tuple[int, int]:
    if not directory.exists():
        print(f"Error: El directorio {directory} no existe")
        return 0, 0

    if not directory.is_dir():
        print(f"Error: {directory} no es un directorio válido")
        return 0, 0

    markdown_files = sorted(_iter_markdown_files(directory))
    if not markdown_files:
        print(f"No se encontraron archivos Markdown en {directory}")
        return 0, 0

    print(f"Se encontraron {len(markdown_files)} archivos Markdown en {directory}")
    print("Iniciando conversión…")

    success = 0
    failed = 0
    for md_file in markdown_files:
        if convert_single_markdown(md_file, output_format, None, highlight_style, resource_dirs):
            success += 1
        else:
            failed += 1

    print("Conversión completada.")
    print(f"  ✓ Exitosas: {success}")
    print(f"  ✗ Fallidas: {failed}")

    return success, failed



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convertir Markdown a PDF o DOCX usando Pandoc",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos:
  python simple_converter.py --file documento.md --format pdf
  python simple_converter.py --file documento.md --format docx --output salida.docx
  python simple_converter.py --directory carpeta/markdowns
        """,
    )

    parser.add_argument(
        "--format",
        "-t",
        default="pdf",
        choices=SUPPORTED_FORMATS,
        help="Formato de salida deseado (pdf o docx)",
    )
    parser.add_argument(
        "--highlight-style",
        default=DEFAULT_HIGHLIGHT_STYLE,
        help="Estilo de resaltado de sintaxis aceptado por Pandoc",
    )
    parser.add_argument(
        "--resource-path",
        action="append",
        default=[],
        metavar="RUTA",
        help="Ruta adicional para resolver recursos (puede repetirse)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Archivo de salida (solo válido con --file)",
    )
    parser.add_argument(
        "--list-highlight-styles",
        action="store_true",
        help="Muestra los estilos de resaltado disponibles y termina",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="Archivo Markdown a convertir")
    group.add_argument(
        "-d",
        "--directory",
        help="Directorio con Markdown a convertir (recursivo)",
    )

    return parser



def main(argv: Sequence[str] | None = None) -> None:
    pandoc_path = _ensure_pandoc()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_highlight_styles:
        styles = _available_highlight_styles(pandoc_path)
        print("Estilos de resaltado disponibles:")
        for style in styles:
            print(f"  - {style}")
        return

    try:
        output_format = _normalise_format(args.format)
    except ValueError as exc:
        parser.error(str(exc))
        return

    extra_resources = [Path(p) for p in args.resource_path]

    if args.output and not args.file:
        parser.error("--output solo puede usarse junto con --file")
        return

    highlight_style = args.highlight_style

    if args.file:
        success = convert_single_markdown(
            Path(args.file),
            output_format,
            Path(args.output) if args.output else None,
            highlight_style,
            extra_resources,
        )
        sys.exit(0 if success else 1)

    if args.directory:
        success, failed = convert_directory(
            Path(args.directory), output_format, highlight_style, extra_resources
        )
        sys.exit(0 if failed == 0 else 1)

    default_path = _default_enunciados_path()
    if default_path is None:
        print(
            "Error: No se encontró la carpeta 'enunciados_sinteticos'. "
            "Proporciona --file o --directory explícitamente."
        )
        sys.exit(1)

    success, failed = convert_directory(
        default_path, output_format, highlight_style, extra_resources
    )
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()

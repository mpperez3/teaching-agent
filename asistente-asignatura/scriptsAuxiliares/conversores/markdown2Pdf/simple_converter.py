#!/usr/bin/env python3
"""Conversor avanzado de Markdown a PDF para el proyecto teaching-agent."""

from __future__ import annotations

import argparse
import sys
from html import escape
from pathlib import Path

from markdown import markdown
from pygments.formatters import HtmlFormatter
from weasyprint import CSS, HTML


BASE_CSS = """
@page {
    size: A4;
    margin: 2.4cm 2.0cm 2.6cm 2.0cm;
    @bottom-right {
        content: "Página " counter(page) " de " counter(pages);
        font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-size: 9pt;
        color: #6b7280;
    }
    @top-left {
        content: string(doc-title);
        font-weight: 600;
        font-size: 10pt;
        color: #4b5563;
    }
}

html {
    font-size: 12pt;
}

body {
    color: #1f2933;
    font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 1rem;
    line-height: 1.6;
    background: #ffffff;
    string-set: doc-title attr(data-title);
}

body, h1, h2, h3, h4, h5, h6, p {
    margin: 0;
    padding: 0;
}

article.document {
    display: block;
    width: 100%;
}

.document__header {
    margin-bottom: 1.2rem;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 0.8rem;
}

.document__header h1 {
    font-size: 2.1rem;
    font-weight: 700;
    color: #111827;
}

h1 {
    margin: 0 0 0.8rem 0;
    font-size: 2.1rem;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.015em;
    string-set: doc-title content();
}

h2 {
    margin: 1.4rem 0 0.6rem 0;
    font-size: 1.55rem;
    font-weight: 600;
    color: #1f2937;
}

h3 {
    margin: 1.2rem 0 0.5rem 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
}

h4, h5, h6 {
    margin: 1rem 0 0.4rem 0;
    font-weight: 600;
    color: #1f2937;
}

p {
    margin: 0 0 0.75rem 0;
    font-size: 1rem;
}

strong {
    color: #111827;
    font-weight: 600;
}

em {
    color: #374151;
}

ul, ol {
    margin: 0 0 0.75rem 1.2rem;
    padding-left: 0.4rem;
}

li {
    margin-bottom: 0.35rem;
    font-size: 1rem;
}

li::marker {
    color: #3b82f6;
    font-weight: 600;
}

blockquote {
    margin: 0.9rem 0;
    padding: 0.6rem 1rem;
    border-left: 4px solid #3b82f6;
    background: #f8fafc;
    color: #374151;
    font-style: italic;
}

code {
    font-family: 'Fira Code', 'JetBrains Mono', 'SFMono-Regular', 'Consolas', 'Menlo', monospace;
    background: #f3f4f6;
    padding: 0.08rem 0.35rem;
    border-radius: 4px;
    font-size: 0.95rem;
}

pre code {
    padding: 0;
    background: transparent;
    font-size: 0.95rem;
}

.codehilite {
    margin: 1rem 0 1.3rem 0;
    padding: 1rem 1.1rem;
    border-radius: 10px;
    border: 1px solid #d1d5db;
    background: #f9fafb;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.06);
}

.codehilite pre {
    margin: 0;
    overflow-wrap: normal;
    white-space: pre;
}

.codehilite::-webkit-scrollbar {
    height: 6px;
}

.codehilite::-webkit-scrollbar-thumb {
    background: #9ca3af;
    border-radius: 3px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.2rem 0;
    font-size: 0.97rem;
}

th, td {
    border: 1px solid #d1d5db;
    padding: 0.55rem 0.75rem;
    text-align: left;
}

th {
    background: #f3f4f6;
    color: #111827;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.035em;
}

tr:nth-child(even) td {
    background: #f9fafb;
}

a {
    color: #2563eb;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

img {
    max-width: 100%;
    display: block;
    margin: 1rem auto;
    border-radius: 8px;
}

hr {
    border: none;
    border-top: 1px solid #d1d5db;
    margin: 1.5rem 0;
}

.toc {
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 1rem;
    background: #f9fafb;
    margin: 1.5rem 0;
}

.toc ul {
    margin: 0.4rem 0 0 1.1rem;
}

.toc li {
    margin-bottom: 0.25rem;
}
"""


def _build_stylesheet() -> str:
    formatter = HtmlFormatter(style="friendly", linenos=False)
    highlight_css = formatter.get_style_defs(".codehilite")
    # Ajustes adicionales para un contraste equilibrado.
    extra_code_css = """
.codehilite .hll { background-color: #fef3c7; }
.codehilite span { font-size: 0.95rem; }
"""
    return "\n".join([BASE_CSS.strip(), highlight_css, extra_code_css.strip()])


def _build_html_document(markdown_text: str, title: str, stylesheet: str) -> str:
    html_body = markdown(
        markdown_text,
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
            "sane_lists",
        ],
        extension_configs={
            "codehilite": {
                "guess_lang": True,
                "noclasses": False,
                "pygments_style": "friendly",
                "linenums": False,
            },
            "toc": {"permalink": "#"},
        },
    )

    safe_title = escape(title)
    return f"""<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"utf-8\">
    <title>{safe_title}</title>
    <style>
    {stylesheet}
    </style>
</head>
<body data-title=\"{safe_title}\">
    <article class=\"document\">
        <div class=\"document__header\">
            <h1>{safe_title}</h1>
        </div>
        <div class=\"document__content\">
            {html_body}
        </div>
    </article>
</body>
</html>"""


def _infer_title(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("# ").strip() or fallback
    return fallback


def convert_markdown_to_pdf(markdown_path: Path) -> Path:
    markdown_text = markdown_path.read_text(encoding="utf-8")
    title = _infer_title(markdown_text, markdown_path.stem)
    stylesheet = _build_stylesheet()
    html_document = _build_html_document(markdown_text, title, stylesheet)

    output_path = markdown_path.with_suffix(".pdf")
    HTML(string=html_document, base_url=str(markdown_path.parent)).write_pdf(
        str(output_path), stylesheets=[CSS(string=stylesheet)]
    )

    return output_path


def convert_single_markdown(markdown_file: Path) -> bool:
    if not markdown_file.exists():
        print(f"Error: El archivo {markdown_file} no existe")
        return False

    if markdown_file.suffix.lower() != ".md":
        print(f"Error: El archivo {markdown_file} no es un Markdown")
        return False

    try:
        print(f"Convirtiendo: {markdown_file.name}")
        pdf_path = convert_markdown_to_pdf(markdown_file)
        print(f"✓ Creado: {pdf_path.name}")
        return True
    except Exception as exc:  # pragma: no cover - ejecución manual
        print(f"✗ Error al convertir {markdown_file.name}: {exc}")
        return False


def convert_directory_markdowns(directory: Path) -> tuple[int, int]:
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
        if convert_single_markdown(md_file):
            success += 1
        else:
            failed += 1

    print("-" * 50)
    print("Conversión completada:")
    print(f"  ✓ Exitosas: {success}")
    print(f"  ✗ Fallidas: {failed}")

    return success, failed


def convert_all_markdowns() -> tuple[int, int]:
    script_dir = Path(__file__).parent
    base_path = script_dir.parent.parent.parent / "ejercicios" / "enunciados_sinteticos"
    if not base_path.exists():
        print(f"Error: La ruta base {base_path} no existe")
        return 0, 0
    return convert_directory_markdowns(base_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convertir archivos Markdown a PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python simple_converter.py                    # Convierte todos los Markdown de enunciados_sinteticos
  python simple_converter.py -f documento.md    # Convierte un único archivo Markdown
  python simple_converter.py -d carpeta         # Convierte todos los Markdown en una carpeta (recursivo)
        """,
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="Archivo Markdown a convertir")
    group.add_argument(
        "-d",
        "--directory",
        help="Directorio que contiene Markdown (incluye subdirectorios)",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.file:
        success = convert_single_markdown(Path(args.file))
        sys.exit(0 if success else 1)

    if args.directory:
        success, failed = convert_directory_markdowns(Path(args.directory))
        sys.exit(0 if failed == 0 else 1)

    success, failed = convert_all_markdowns()
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()

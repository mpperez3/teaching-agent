#!/usr/bin/env python3
"""Conversor avanzado de Markdown a PDF para el proyecto teaching-agent."""

from __future__ import annotations

import argparse
import sys
from html import escape
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup
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

:root {
    --color-primary: #2563eb;
    --color-secondary: #4b5563;
    --color-muted: #6b7280;
    --border-color: #d1d5db;
    --background-soft: #f8fafc;
    --font-base: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    --font-mono: 'Fira Code', 'JetBrains Mono', 'SFMono-Regular', 'Consolas', 'Menlo', monospace;
}

html {
    font-size: 12pt;
}

body {
    color: #1f2933;
    font-family: var(--font-base);
    font-size: 1rem;
    line-height: 1.65;
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
    margin-bottom: 1.5rem;
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 1rem;
}

.document__header h1 {
    font-size: 2.25rem;
    font-weight: 700;
    color: #0f172a;
}

h1 {
    margin: 0 0 1rem 0;
    font-size: 2.25rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.015em;
    string-set: doc-title content();
    page-break-after: avoid;
}

h2 {
    margin: 1.6rem 0 0.7rem 0;
    font-size: 1.65rem;
    font-weight: 600;
    color: #111827;
    page-break-after: avoid;
}

h3 {
    margin: 1.35rem 0 0.55rem 0;
    font-size: 1.3rem;
    font-weight: 600;
    color: #111827;
    page-break-after: avoid;
}

h4, h5, h6 {
    margin: 1.2rem 0 0.45rem 0;
    font-weight: 600;
    color: #1f2937;
    page-break-after: avoid;
}

p {
    margin: 0 0 0.85rem 0;
    font-size: 1rem;
}

strong {
    color: #111827;
    font-weight: 650;
}

em {
    color: #374151;
}

ul, ol {
    margin: 0 0 0.85rem 1.3rem;
    padding-left: 0.4rem;
}

li {
    margin-bottom: 0.35rem;
    font-size: 1rem;
}

li::marker {
    color: var(--color-primary);
    font-weight: 600;
}

blockquote {
    margin: 1.1rem 0;
    padding: 0.7rem 1.1rem;
    border-left: 4px solid var(--color-primary);
    background: var(--background-soft);
    color: #1f2937;
    font-style: italic;
    box-shadow: inset 0 0 0 1px rgba(37, 99, 235, 0.08);
}

code {
    font-family: var(--font-mono);
    background: #f3f4f6;
    padding: 0.08rem 0.4rem;
    border-radius: 4px;
    font-size: 0.95rem;
}

pre code {
    padding: 0;
    background: transparent;
    font-size: 0.95rem;
}

.codehilite {
    position: relative;
    margin: 1.1rem 0 1.4rem 0;
    padding: 1.2rem 1.25rem 1rem 1.25rem;
    border-radius: 14px;
    border: 1px solid var(--border-color);
    background: var(--background-soft);
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.09);
    overflow: hidden;
    --code-accent: #334155;
    --code-background: #f8fafc;
}

.codehilite::before {
    content: attr(data-language);
    position: absolute;
    top: 0;
    left: 0;
    padding: 0.45rem 0.9rem;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    font-weight: 700;
    text-transform: uppercase;
    background: var(--code-accent);
    color: #ffffff;
    border-bottom-right-radius: 10px;
}

.codehilite pre {
    margin: 0;
    white-space: pre;
    background: var(--code-background);
    border-radius: 8px;
    padding: 0.9rem 0.7rem 0.9rem 0.7rem;
}

.codehilite table {
    width: 100%;
    border-collapse: collapse;
}

.codehilite td {
    border: none;
    padding: 0;
}

.codehilite .linenos {
    padding-right: 0.9rem;
    border-right: 1px solid rgba(148, 163, 184, 0.35);
    color: #94a3b8;
}

.codehilite .linenos pre {
    background: transparent;
    padding-right: 0.75rem;
}

.codehilite::-webkit-scrollbar {
    height: 6px;
}

.codehilite::-webkit-scrollbar-thumb {
    background: #9ca3af;
    border-radius: 3px;
}

.codehilite.language-python,
.codehilite[data-language="PYTHON"] {
    --code-accent: #2563eb;
    --code-background: #eff6ff;
}

.codehilite.language-java,
.codehilite[data-language="JAVA"] {
    --code-accent: #ea580c;
    --code-background: #fff7ed;
}

.codehilite.language-c,
.codehilite[data-language="C"] {
    --code-accent: #059669;
    --code-background: #ecfdf5;
}

.codehilite.language-cpp,
.codehilite[data-language="CPP"],
.codehilite.language-c-plus-plus {
    --code-accent: #0ea5e9;
    --code-background: #e0f2fe;
}

.codehilite .code-content {
    font-family: var(--font-mono);
    font-size: 0.94rem;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.35rem 0;
    font-size: 0.97rem;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
}

th, td {
    border: 1px solid var(--border-color);
    padding: 0.6rem 0.85rem;
    text-align: left;
}

th {
    background: #eef2ff;
    color: #1e1b4b;
    font-weight: 650;
    text-transform: uppercase;
    letter-spacing: 0.035em;
}

tr:nth-child(even) td {
    background: #f8fafc;
}

caption {
    caption-side: bottom;
    text-align: center;
    font-size: 0.9rem;
    color: var(--color-muted);
    margin-top: 0.6rem;
}

a {
    color: var(--color-primary);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

img {
    max-width: 100%;
    display: block;
    margin: 1rem auto;
    border-radius: 12px;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.12);
}

figure {
    margin: 1.2rem auto;
    text-align: center;
}

figcaption {
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: var(--color-muted);
}

hr {
    border: none;
    border-top: 1px solid var(--border-color);
    margin: 1.75rem 0;
}

.toc {
    border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    background: #eef2ff;
    margin: 1.75rem 0;
    box-shadow: 0 8px 22px rgba(37, 99, 235, 0.12);
}

.toc > ul {
    margin: 0.4rem 0 0 1.1rem;
}

.toc li {
    margin-bottom: 0.25rem;
}

mark {
    background: #fef08a;
    padding: 0.1rem 0.25rem;
    border-radius: 4px;
}

kbd {
    font-family: var(--font-mono);
    font-size: 0.85rem;
    background: #e2e8f0;
    border-radius: 6px;
    padding: 0.15rem 0.4rem;
    border: 1px solid rgba(148, 163, 184, 0.7);
    box-shadow: inset 0 -2px 0 rgba(15, 23, 42, 0.1);
}
"""


def _build_stylesheet() -> str:
    formatter = HtmlFormatter(
        style="material",
        linenos="table",
        cssclass="codehilite",
        wrapcode=True,
    )
    highlight_css = formatter.get_style_defs(".codehilite")
    extra_code_css = """
.codehilite .hll { background-color: rgba(250, 204, 21, 0.25); }
.codehilite span { font-size: 0.94rem; }
"""
    return "\n".join([BASE_CSS.strip(), highlight_css, extra_code_css.strip()])


def _normalise_language_name(raw_language: str | None) -> str:
    if not raw_language:
        return "Texto"

    language = raw_language.strip().lower()
    aliases = {
        "py": "Python",
        "py3": "Python",
        "python": "Python",
        "java": "Java",
        "c": "C",
        "c++": "CPP",
        "cpp": "CPP",
        "cxx": "CPP",
        "sh": "Shell",
        "bash": "Shell",
        "json": "JSON",
        "yaml": "YAML",
        "yml": "YAML",
        "txt": "Texto",
    }

    if language in aliases:
        return aliases[language]

    return language.upper()


def _extract_language_from_classes(classes: Iterable[str]) -> str | None:
    for class_name in classes:
        if class_name.startswith("language-"):
            return class_name.split("-", 1)[1]
        if class_name in {"python", "java", "c", "cpp"}:
            return class_name
    return None


def _enhance_code_blocks(html_fragment: str) -> str:
    soup = BeautifulSoup(html_fragment, "html.parser")

    for block in soup.select("div.codehilite"):
        block_classes = list(block.get("class", []))
        language = _extract_language_from_classes(block_classes)

        if language is None:
            code_node = block.find("code")
            if code_node:
                language = _extract_language_from_classes(code_node.get("class", []))

        label = _normalise_language_name(language)
        block["data-language"] = label

        if language:
            lang_class = f"language-{language.lower()}"
            if lang_class not in block_classes:
                block_classes.append(lang_class)
                block["class"] = block_classes

        code_content = block.find("code")
        if code_content:
            existing = list(code_content.get("class", []))
            if "code-content" not in existing:
                code_content["class"] = [*existing, "code-content"]

    return str(soup)


def _build_html_document(markdown_text: str, title: str, stylesheet: str) -> str:
    html_body = markdown(
        markdown_text,
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
            "sane_lists",
            "attr_list",
            "def_list",
            "footnotes",
            "md_in_html",
            "admonition",
        ],
        extension_configs={
            "codehilite": {
                "guess_lang": True,
                "noclasses": False,
                "pygments_style": "material",
                "linenums": True,
            },
            "toc": {"permalink": "#"},
        },
    )

    html_body = _enhance_code_blocks(html_body)

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
    candidate_roots = [
        script_dir.parent.parent.parent / "ejercicios" / "enunciados_sinteticos",
        script_dir.parent.parent.parent / "enunciados_sinteticos",
    ]

    for base_path in candidate_roots:
        if base_path.exists():
            return convert_directory_markdowns(base_path)

    print(
        "Error: No se encontró la carpeta 'enunciados_sinteticos'. "
        "Revise la estructura del proyecto."
    )
    return 0, 0


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

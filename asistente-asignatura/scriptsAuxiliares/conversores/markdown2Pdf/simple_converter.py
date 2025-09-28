#!/usr/bin/env python3
"""
Markdown to PDF converter for the teaching assistant project.

The converter focuses on producing readable PDFs from Markdown notes
while preserving headings, lists and code blocks with appropriate
formatting.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, List

from bs4 import BeautifulSoup, NavigableString, Tag
from markdown import markdown
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer


def _create_styles() -> dict[str, ParagraphStyle]:
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontSize=11,
            leading=14,
        )
    )
    
    styles.add(
        ParagraphStyle(
            name="CustomCode",
            fontName="Courier",
            fontSize=9,
            leading=11,
            leftIndent=12,
            rightIndent=12,
            backColor=colors.whitesmoke,
            borderColor=colors.lightgrey,
            borderWidth=0.25,
            borderPadding=6,
            spaceBefore=6,
            spaceAfter=6,
        )
    )
    
    styles.add(
        ParagraphStyle(
            name="BlockQuote",
            parent=styles["Body"],
            leftIndent=18,
            textColor=colors.HexColor("#444444"),
            spaceBefore=6,
            spaceAfter=6,
            italic=True,
        )
    )

    # Indentation levels for unordered/ordered lists
    for level in range(4):
        indent = 18 + level * 12
        styles.add(
            ParagraphStyle(
                name=f"ListLevel{level}",
                parent=styles["Body"],
                leftIndent=indent,
                bulletIndent=indent - 9,
                spaceBefore=2,
                spaceAfter=2,
            )
        )

    return styles


def _render_inline_content(element: Tag) -> str:
    """Return HTML string for inline content of an element."""
    return element.decode_contents(formatter="html")


def _render_list_items(
    list_element: Tag,
    styles: dict[str, ParagraphStyle],
    level: int,
    ordered: bool,
) -> List:
    flowables: List = []
    children = list_element.find_all("li", recursive=False)

    for index, item in enumerate(children, start=1):
        bullet = f"{index}." if ordered else "•"
        content_parts = []
        for child in item.contents:
            if isinstance(child, NavigableString):
                content_parts.append(str(child))
            elif isinstance(child, Tag) and child.name not in {"ul", "ol"}:
                content_parts.append(child.decode(formatter="html"))
        text = "".join(content_parts).strip() or "&nbsp;"
        style_name = f"ListLevel{min(level, 3)}"
        flowables.append(Paragraph(text, styles[style_name], bulletText=bullet))

        # Handle nested lists recursively
        for child in item.contents:
            if isinstance(child, Tag) and child.name in {"ul", "ol"}:
                flowables.extend(
                    _render_list_items(
                        child,
                        styles,
                        level + 1,
                        ordered=(child.name == "ol"),
                    )
                )
    flowables.append(Spacer(1, 0.08 * inch))
    return flowables


def _render_element(element: Tag, styles: dict[str, ParagraphStyle]) -> Iterable:
    name = element.name

    if name is None:
        text = str(element).strip()
        if text:
            yield Paragraph(text, styles["Body"])
            yield Spacer(1, 0.08 * inch)
        return

    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        heading_level = int(name[1])
        heading_style = styles.get(f"Heading{min(heading_level, 3)}", styles["Heading1"])
        text = element.get_text(strip=True)
        yield Paragraph(text, heading_style)
        yield Spacer(1, 0.12 * inch)
        return

    if name == "p":
        content = _render_inline_content(element).strip()
        if content:
            yield Paragraph(content, styles["Body"])
            yield Spacer(1, 0.08 * inch)
        return

    if name == "pre":
        code_text = element.get_text().rstrip("\n")
        if code_text:
            yield Preformatted(code_text, styles["CustomCode"])
            yield Spacer(1, 0.1 * inch)
        return

    if name == "blockquote":
        text = _render_inline_content(element).strip()
        if text:
            yield Paragraph(text, styles["BlockQuote"])
            yield Spacer(1, 0.08 * inch)
        return

    if name == "ul":
        yield from _render_list_items(element, styles, level=0, ordered=False)
        return

    if name == "ol":
        yield from _render_list_items(element, styles, level=0, ordered=True)
        return

    if name == "hr":
        yield Spacer(1, 0.15 * inch)
        return

    if name == "table":
        rows = []
        for row in element.find_all("tr"):
            cells = [cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])]
            if cells:
                rows.append(" | ".join(cells))
        if rows:
            table_text = "\n".join(rows)
            yield Preformatted(table_text, styles["CustomCode"])
            yield Spacer(1, 0.1 * inch)
        return

    # Fallback: render children sequentially
    for child in element.children:
        if isinstance(child, (Tag, NavigableString)):
            yield from _render_element(child, styles)


def markdown_to_flowables(markdown_text: str) -> List:
    html = markdown(
        markdown_text,
        extensions=[
            "fenced_code",
            "tables",
            "sane_lists",
        ],
    )
    soup = BeautifulSoup(html, "html.parser")
    styles = _create_styles()

    flowables: List = []
    for element in soup.contents:
        if isinstance(element, (Tag, NavigableString)):
            flowables.extend(list(_render_element(element, styles)))

    if not flowables:
        flowables.append(Paragraph("(Documento sin contenido)", styles["Body"]))

    return flowables


def convert_markdown_to_pdf(markdown_path: Path) -> Path:
    markdown_text = markdown_path.read_text(encoding="utf-8")
    flowables = markdown_to_flowables(markdown_text)

    output_path = markdown_path.with_suffix(".pdf")
    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=0.9 * inch,
        rightMargin=0.9 * inch,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch,
        title=markdown_path.stem,
    )
    document.build(flowables)

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
    base_path = script_dir.parent.parent.parent / "enunciados_sinteticos"
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

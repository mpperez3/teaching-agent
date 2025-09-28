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
from typing import Iterable, List, Optional

from bs4 import BeautifulSoup, NavigableString, Tag
from markdown import markdown
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer

try:  # Syntax highlighting is optional
    from pygments import lex
    from pygments.lexers import TextLexer, get_lexer_by_name, guess_lexer
    from pygments.token import Token
    from pygments.util import ClassNotFound

    PYGMENTS_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    PYGMENTS_AVAILABLE = False
    Token = None  # type: ignore


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
            backColor=colors.HexColor("#f6f8fa"),
            borderColor=colors.lightgrey,
            borderWidth=0.25,
            borderPadding=6,
            spaceBefore=6,
            spaceAfter=6,
            textColor=colors.HexColor("#2f2f2f"),
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


DEFAULT_CODE_COLOR = colors.HexColor("#2f2f2f")

if PYGMENTS_AVAILABLE:
    TOKEN_COLOR_MAP = [
        (Token.Comment, colors.HexColor("#6a737d")),
        (Token.Keyword, colors.HexColor("#d73a49")),
        (Token.Operator, colors.HexColor("#d73a49")),
        (Token.Name.Function, colors.HexColor("#005cc5")),
        (Token.Name.Class, colors.HexColor("#6f42c1")),
        (Token.Name.Builtin, colors.HexColor("#005cc5")),
        (Token.Name.Decorator, colors.HexColor("#6f42c1")),
        (Token.Literal.String, colors.HexColor("#032f62")),
        (Token.Literal.Number, colors.HexColor("#005cc5")),
        (Token.Name.Attribute, colors.HexColor("#24292e")),
        (Token.Punctuation, colors.HexColor("#24292e")),
    ]
else:  # pragma: no cover - sin pygments
    TOKEN_COLOR_MAP = []


class CodeBlockFlowable(Flowable):
    """Render code blocks with optional syntax highlighting and soft wrapping."""

    def __init__(
        self,
        token_lines: List[List[tuple[colors.Color, str]]],
        style: ParagraphStyle,
    ) -> None:
        super().__init__()
        self._original_lines = token_lines or [[(DEFAULT_CODE_COLOR, "")]]
        self.style = style
        self._wrapped_lines: List[List[tuple[colors.Color, str]]] = []
        self._available_width: Optional[float] = None
        self._content_width: float = 0.0
        self._block_width: float = 0.0
        self._line_height: float = float(style.leading or (style.fontSize * 1.2))
        self._padding: float = float(getattr(style, "borderPadding", 4))
        self._border_width: float = float(getattr(style, "borderWidth", 0))
        self.height: float = 0.0

    def wrap(self, availWidth: float, availHeight: float) -> tuple[float, float]:
        if availWidth != self._available_width:
            self._layout_lines(availWidth)
        return availWidth, self.height

    def _layout_lines(self, avail_width: float) -> None:
        self._available_width = avail_width
        left_indent = float(getattr(self.style, "leftIndent", 0))
        right_indent = float(getattr(self.style, "rightIndent", 0))
        usable_width = max(avail_width - left_indent - right_indent, 12.0)
        inner_width = max(usable_width - 2 * self._padding, 4.0)

        char_width = pdfmetrics.stringWidth("M", self.style.fontName, self.style.fontSize)
        max_chars = max(1, int(inner_width // max(char_width, 0.1)))

        wrapped_lines: List[List[tuple[colors.Color, str]]] = []
        for line_tokens in self._original_lines:
            wrapped_lines.extend(self._wrap_line_tokens(line_tokens, max_chars))

        if not wrapped_lines:
            wrapped_lines = [[(DEFAULT_CODE_COLOR, "")]]

        self._wrapped_lines = wrapped_lines
        self._content_width = inner_width
        self._block_width = inner_width + 2 * self._padding
        line_count = len(self._wrapped_lines)
        content_height = max(1, line_count) * self._line_height
        self.height = content_height + 2 * self._padding + 2 * self._border_width

    def _wrap_line_tokens(
        self,
        line_tokens: List[tuple[colors.Color, str]],
        max_chars: int,
    ) -> List[List[tuple[colors.Color, str]]]:
        if not line_tokens:
            return [[]]

        wrapped: List[List[tuple[colors.Color, str]]] = []
        current_line: List[tuple[colors.Color, str]] = []
        current_length = 0

        for color, segment in line_tokens:
            text = segment.replace("\t", "    ")
            while text:
                remaining = max_chars - current_length
                if remaining <= 0:
                    wrapped.append(current_line)
                    current_line = []
                    current_length = 0
                    remaining = max_chars

                chunk = text[:remaining]
                current_line.append((color, chunk))
                current_length += len(chunk)
                text = text[remaining:]

                if text:
                    wrapped.append(current_line)
                    current_line = []
                    current_length = 0

        wrapped.append(current_line)
        return wrapped

    def draw(self) -> None:  # pragma: no cover - rendering
        canvas = self.canv
        canvas.saveState()

        left_indent = float(getattr(self.style, "leftIndent", 0))
        padding = self._padding
        block_x = left_indent
        block_y = 0
        block_height = self.height
        block_width = self._block_width

        back_color = self.style.backColor or colors.whitesmoke
        border_color = self.style.borderColor or colors.transparent

        canvas.setFillColor(back_color)
        canvas.setStrokeColor(back_color)
        canvas.rect(block_x, block_y, block_width, block_height, stroke=0, fill=1)

        if self._border_width > 0:
            canvas.setLineWidth(self._border_width)
            canvas.setStrokeColor(border_color)
            canvas.rect(block_x, block_y, block_width, block_height, stroke=1, fill=0)

        text_x_start = block_x + padding
        baseline = block_height - padding - self.style.fontSize

        font_name = self.style.fontName
        font_size = self.style.fontSize
        canvas.setFont(font_name, font_size)

        default_color = getattr(self.style, "textColor", DEFAULT_CODE_COLOR)

        for line in self._wrapped_lines:
            x_cursor = text_x_start
            if line:
                for color, segment in line:
                    canvas.setFillColor(color or default_color)
                    canvas.drawString(x_cursor, baseline, segment)
                    segment_width = pdfmetrics.stringWidth(segment, font_name, font_size)
                    x_cursor += segment_width
            baseline -= self._line_height

        canvas.restoreState()


def _color_for_token(token_type) -> colors.Color:
    if not PYGMENTS_AVAILABLE or token_type is None:
        return DEFAULT_CODE_COLOR
    for candidate, color in TOKEN_COLOR_MAP:
        if token_type in candidate:
            return color
    return DEFAULT_CODE_COLOR


def _resolve_code_language(element: Tag) -> Optional[str]:
    code_tag = element.find("code")
    if not code_tag:
        return None

    class_attr = code_tag.get("class", [])
    if isinstance(class_attr, str):
        class_attr = [class_attr]

    for class_name in class_attr:
        if class_name.startswith("language-"):
            return class_name[len("language-") :]
    return None


def _select_lexer(language: Optional[str], code_text: str):  # pragma: no cover - small wrapper
    if not PYGMENTS_AVAILABLE:
        raise RuntimeError("Pygments no disponible")

    if language:
        try:
            return get_lexer_by_name(language)
        except ClassNotFound:
            pass

    try:
        return guess_lexer(code_text)
    except ClassNotFound:
        return TextLexer()


def _tokenize_code(code_text: str, language: Optional[str]) -> List[List[tuple[colors.Color, str]]]:
    if not code_text:
        return [[(DEFAULT_CODE_COLOR, "")]]

    normalized = code_text.replace("\r\n", "\n").replace("\r", "\n")

    if not PYGMENTS_AVAILABLE:
        return [[(DEFAULT_CODE_COLOR, line)] for line in normalized.split("\n")]

    lexer = _select_lexer(language, normalized)
    token_lines: List[List[tuple[colors.Color, str]]] = [[]]

    for token_type, value in lex(normalized, lexer):
        if value == "":
            continue

        value = value.replace("\t", "    ")
        segments = value.split("\n")

        for index, segment in enumerate(segments):
            if segment:
                token_lines[-1].append((_color_for_token(token_type), segment))
            if index < len(segments) - 1:
                token_lines.append([])

    return token_lines or [[(DEFAULT_CODE_COLOR, "")]]


def _build_code_flowable(element: Tag, styles: dict[str, ParagraphStyle]) -> Flowable:
    code_style = styles["CustomCode"]
    language = _resolve_code_language(element)
    code_text = element.get_text().rstrip("\n")
    token_lines = _tokenize_code(code_text, language)
    return CodeBlockFlowable(token_lines, code_style)


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
        yield _build_code_flowable(element, styles)
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
            token_lines = _tokenize_code(table_text, language=None)
            yield CodeBlockFlowable(token_lines, styles["CustomCode"])
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

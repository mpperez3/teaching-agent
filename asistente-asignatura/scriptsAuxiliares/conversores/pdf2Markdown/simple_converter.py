#!/usr/bin/env python3
"""
PDF to Markdown converter using Docling.

Converts PDF files to Markdown format with multiple modes:
- Single file conversion
- Directory conversion (with subdirectories)
- Default: all PDFs in base_de_conocimiento directory

Features:
- Automatic code block detection and improved formatting
- Language tagging for fenced code blocks (Java, Python, C/C++, JavaScript, SQL, ...)
- Friendly CLI with install/update/reinstall helpers handled in the shell wrapper
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

# Path configuration: resolve from project root, never via magic parent traversals
try:
    from ...config import BASE_DE_CONOCIMIENTO  # noqa: E402
except ImportError:
    BASE_DE_CONOCIMIENTO = None  # noqa: F841


from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

from docling_core.types.doc import CodeLanguageLabel, DocItemLabel
from docling_core.types.doc.document import DoclingDocument


CODE_BLOCK_PATTERN = re.compile(r"```(?P<lang>[^\n]*)\n(?P<body>.*?)\n```", re.DOTALL)
CODE_LABEL_MAPPING = {
    CodeLanguageLabel.C: "c",
    CodeLanguageLabel.C_PLUS_PLUS: "cpp",
    CodeLanguageLabel.C_SHARP: "csharp",
    CodeLanguageLabel.JAVA: "java",
    CodeLanguageLabel.JAVASCRIPT: "javascript",
    CodeLanguageLabel.KOTLIN: "kotlin",
    CodeLanguageLabel.PYTHON: "python",
    CodeLanguageLabel.SQL: "sql",
    CodeLanguageLabel.SWIFT: "swift",
    CodeLanguageLabel.TYPESCRIPT: "typescript",
    CodeLanguageLabel.RUST: "rust",
    CodeLanguageLabel.GO: "go",
    CodeLanguageLabel.PHP: "php",
}

LANGUAGE_ALIASES = {
    "c++": "cpp",
    "cpp": "cpp",
    "c": "c",
    "csharp": "csharp",
    "c#": "csharp",
    "java": "java",
    "javascript": "javascript",
    "js": "javascript",
    "typescript": "typescript",
    "ts": "typescript",
    "python": "python",
    "py": "python",
    "sql": "sql",
    "kotlin": "kotlin",
    "swift": "swift",
    "rust": "rust",
    "go": "go",
    "php": "php",
    "objective-c": "objectivec",
    "objectivec": "objectivec",
}

ALLOWED_LANGUAGES = set(LANGUAGE_ALIASES.values())

BROKEN_KEYWORD_FIXES = {
    "p ublic": "public",
    "p rivate": "private",
    "p rotected": "protected",
    "s tatic": "static",
    "c lass": "class",
    "i nterface": "interface",
    "e xtends": "extends",
    "i mplements": "implements",
    "t hrows": "throws",
    "r eturn": "return",
}

Token = Tuple[str, str, Optional[str]]


@dataclass
class CodeGroup:
    texts: List[str]
    label: CodeLanguageLabel


def split_markdown_tokens(markdown: str) -> List[Token]:
    """Split markdown into plain text and fenced code tokens."""

    tokens: List[Token] = []
    cursor = 0
    for match in CODE_BLOCK_PATTERN.finditer(markdown):
        start, end = match.span()
        if start > cursor:
            tokens.append(("text", markdown[cursor:start], None))
        tokens.append(("code", match.group("body"), match.group("lang").strip()))
        cursor = end
    if cursor < len(markdown):
        tokens.append(("text", markdown[cursor:], None))
    return tokens


def extract_code_groups(document: DoclingDocument) -> List[CodeGroup]:
    """Group consecutive code items reported by Docling."""

    groups: List[CodeGroup] = []
    current: Optional[CodeGroup] = None

    for item, _level in document.iterate_items():
        if item.label == DocItemLabel.CODE:
            if current is None:
                current = CodeGroup(texts=[item.text], label=item.code_language)
            else:
                current.texts.append(item.text)
                if (
                    current.label == CodeLanguageLabel.UNKNOWN
                    and item.code_language != CodeLanguageLabel.UNKNOWN
                ):
                    current.label = item.code_language
        else:
            if current is not None:
                groups.append(current)
                current = None

    if current is not None:
        groups.append(current)

    return groups


def heuristic_language_detection(code: str) -> str:
    """Backup language detection using simple keyword heuristics."""

    lookup = {
        "java": [
            "public class",
            "public interface",
            "public boolean",
            "public static",
            "public ",
            "implements",
            "extends",
            "system.out",
            "@override",
            " new arraylist",
            "lista<",
        ],
        "python": ["def ", "class ", "self", "print(", "import "],
        "cpp": ["#include", "std::", "cout <<", "cin >>", "using namespace"],
        "c": ["#include", "printf(", "scanf(", "malloc(", "struct "],
        "javascript": ["function ", "const ", "let ", "=>", "console.log"],
        "sql": ["select ", "from ", "where ", "join ", "order by"],
    }

    best_lang = ""
    best_score = 0
    lower = code.lower()

    for lang, patterns in lookup.items():
        score = sum(3 for pattern in patterns if pattern in lower)
        if score > best_score:
            best_lang = lang
            best_score = score

    return best_lang if best_score >= 3 else ""


def normalize_language_name(name: str) -> str:
    if not name:
        return ""
    lowered = name.lower()
    mapped = LANGUAGE_ALIASES.get(lowered)
    if mapped:
        return mapped
    return lowered if lowered in ALLOWED_LANGUAGES else ""


def normalize_text_segment(text: str) -> str:
    unescaped = html.unescape(text)
    lines = []
    for line in unescaped.split('\n'):
        cleaned = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', line)
        lines.append(cleaned)
    return '\n'.join(lines)


def postprocess_code_spacing(code: str) -> str:
    lines = []
    for raw_line in code.split('\n'):
        line = raw_line
        for broken, fixed in BROKEN_KEYWORD_FIXES.items():
            line = line.replace(broken, fixed)
        line = re.sub(r'(?<=\w)\s+\(', '(', line)
        line = re.sub(r'\(\s+', '(', line)
        line = re.sub(r'\s+\)', ')', line)
        line = re.sub(r'<\s+', '<', line)
        line = re.sub(r'\s+>', '>', line)
        line = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', line)
        line = re.sub(r'//\s+', '// ', line)
        line = re.sub(r'\b(if|while|for|switch)\(', r'\1 (', line)
        if line.strip().startswith(('else', 'catch', 'finally')):
            prev_indent = 0
            if lines:
                last_line = lines[-1]
                prev_indent = len(last_line) - len(last_line.lstrip(' '))
            line = ' ' * prev_indent + line.strip()
        lines.append(line.rstrip())
    return '\n'.join(lines)


def preprocess_brace_code(code: str) -> str:
    text = code
    text = re.sub(r'\s*//', '\n//', text)
    text = re.sub(r'\s*/\*', '\n/*', text)
    text = re.sub(r'\*/\s*', '*/\n', text)
    text = re.sub(r'(//[^\n]*)\s+(?=\S)', r'\1\n', text)
    text = re.sub(r'(//[^\n]*)\n{2,}', r'\1\n', text)

    keyword_pattern = r'(?<!\n)\s+(?=(?:public|private|protected|if|else|switch|case|default|while|for|return|try|catch|finally)\b)'
    text = re.sub(keyword_pattern, '\n', text)
    class_pattern = r'(?<!\n)(?<!public)(?<!private)(?<!protected)\s+(?=(?:class|interface|enum)\b)'
    text = re.sub(class_pattern, '\n', text)
    text = re.sub(r'(?<!\n)\s+(?=@Override\b)', '\n', text)
    text = re.sub(r'else\s*{', 'else\n{', text)
    text = re.sub(r'\n{2,}', '\n', text)
    return text


def guess_language_from_text(
    code: str,
    *,
    hint: Optional[str] = None,
    code_label: Optional[CodeLanguageLabel] = None,
) -> str:
    """Best-effort language detection combining hints, doc labels and pygments."""

    if hint:
        normalized = normalize_language_name(hint.strip())
        if normalized:
            return normalized

    if code_label and code_label != CodeLanguageLabel.UNKNOWN:
        mapped = CODE_LABEL_MAPPING.get(code_label)
        normalized = normalize_language_name(mapped or code_label.value)
        if normalized:
            return normalized

    candidate = ""
    try:
        lexer = guess_lexer(code)
        aliases = getattr(lexer, "aliases", []) or []
        candidate = normalize_language_name(aliases[0] if aliases else lexer.name)
    except ClassNotFound:
        candidate = ""

    if candidate:
        return candidate

    return normalize_language_name(heuristic_language_detection(code))


def tokenize_brace_code(code: str) -> List[str]:
    tokens: List[str] = []
    buffer = ""
    idx = 0
    length = len(code)

    while idx < length:
        ch = code[idx]
        buffer += ch

        if ch == '/' and idx + 1 < length and code[idx + 1] == '/':
            buffer += '/'
            idx += 2
            while idx < length and code[idx] != '\n':
                buffer += code[idx]
                idx += 1
            tokens.append(buffer.strip())
            buffer = ""
            continue

        if ch == '/' and idx + 1 < length and code[idx + 1] == '*':
            buffer += '*'
            idx += 2
            while idx < length:
                buffer += code[idx]
                if code[idx] == '*' and idx + 1 < length and code[idx + 1] == '/':
                    buffer += '/'
                    idx += 2
                    break
                idx += 1
            tokens.append(buffer.strip())
            buffer = ""
            continue

        if ch == ';':
            tokens.append(buffer.strip())
            buffer = ""
        elif ch == '{':
            pre = buffer[:-1].strip()
            if pre:
                tokens.append(pre)
            tokens.append('{')
            buffer = ""
        elif ch == '}':
            pre = buffer[:-1].strip()
            if pre:
                tokens.append(pre)
            tokens.append('}')
            buffer = ""
        elif ch == '\n':
            if buffer.strip():
                tokens.append(buffer.strip())
                buffer = ""

        idx += 1

    if buffer.strip():
        tokens.append(buffer.strip())

    return [token for token in tokens if token]


def format_brace_code(code: str) -> str:
    tokens = tokenize_brace_code(code)
    if not tokens:
        return code.strip()

    formatted: List[str] = []
    indent = 0

    for token in tokens:
        stripped = token.strip()
        lowered = stripped.lower()

        if stripped == '}':
            indent = max(indent - 1, 0)
            formatted.append('    ' * indent + stripped)
            continue

        if stripped == '{':
            formatted.append('    ' * indent + '{')
            indent += 1
            continue

        if lowered.startswith(('else', 'catch', 'finally')) and formatted:
            last_line = formatted[-1].strip()
            if last_line == '}':
                formatted.append('    ' * indent + stripped)
                continue

        formatted.append('    ' * indent + stripped)

        if stripped.endswith('{'):
            indent += 1
        elif stripped.endswith('}'):
            indent = max(indent - 1, 0)

    result = '\n'.join(line.rstrip() for line in formatted)
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = re.sub(r'\}\s*\n\s*else', '}\nelse', result)
    return result.strip()


def format_python_code(code: str) -> str:
    working = code.replace('\r', '\n').replace('\t', '    ')
    working = re.sub(r'(?<!\n)(@\w[\w\.]*)', r'\n\1', working)
    working = re.sub(r'(?<!\n)(def|class)\s+', r'\n\1 ', working)
    working = re.sub(r':\s*(?=\S)', ':\n', working)
    working = re.sub(r';\s*', ';\n', working)
    working = re.sub(r'\n{2,}', '\n', working)

    lines = [line.strip() for line in working.split('\n')]
    formatted: List[str] = []
    indent = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if formatted and formatted[-1]:
                formatted.append('')
            continue

        lowered = stripped.lower()
        if lowered.startswith(('elif ', 'else', 'except', 'finally')):
            indent = max(indent - 1, 0)

        formatted.append('    ' * indent + stripped)

        if stripped.endswith(':') and not stripped.startswith(('return', 'raise', 'break', 'continue', 'pass', '#')):
            indent += 1

    result = '\n'.join(formatted)
    return re.sub(r'\n{3,}', '\n\n', result).strip()


def format_sql_code(code: str) -> str:
    working = code.replace('\r', ' ').replace('\n', ' ')
    keywords = [
        'SELECT',
        'FROM',
        'WHERE',
        'JOIN',
        'INNER JOIN',
        'LEFT JOIN',
        'RIGHT JOIN',
        'FULL JOIN',
        'GROUP BY',
        'ORDER BY',
        'HAVING',
        'ON',
        'AND',
        'OR',
        'INSERT INTO',
        'VALUES',
        'UPDATE',
        'DELETE FROM',
        'SET',
    ]

    for keyword in keywords:
        pattern = re.compile(rf'(?i)\b{re.escape(keyword)}\b')
        working = pattern.sub(lambda match: '\n' + keyword, working)

    lines = [line.strip() for line in working.split('\n') if line.strip()]
    return '\n'.join(lines)


def normalize_generic_code(code: str) -> str:
    stripped = code.strip()
    if not stripped:
        return ''

    if any(symbol in stripped for symbol in ['{', '}', ';']):
        return format_brace_code(stripped)

    if ':' in stripped and ('def ' in stripped or 'class ' in stripped):
        return format_python_code(stripped)

    return '\n'.join(line.strip() for line in stripped.splitlines())


def format_code_text(code: str, language: str) -> str:
    normalized = html.unescape(code).replace('\r', '\n').strip('\n')
    language_lower = language.lower()

    brace_langs = {'java', 'c', 'cpp', 'c++', 'csharp', 'c#', 'javascript', 'typescript', 'kotlin', 'go', 'swift', 'rust', 'php'}
    if language_lower in brace_langs:
        prepared = preprocess_brace_code(normalized)
        formatted = format_brace_code(prepared)
        return postprocess_code_spacing(formatted)

    if language_lower.startswith('sql'):
        return postprocess_code_spacing(format_sql_code(normalized))

    if language_lower == 'python':
        return postprocess_code_spacing(format_python_code(normalized))

    if any(ch in normalized for ch in '{};'):
        generic = preprocess_brace_code(normalized)
    else:
        generic = normalized
    return postprocess_code_spacing(normalize_generic_code(generic))


def merge_code_tokens(tokens: Sequence[Token], groups: Sequence[CodeGroup]) -> List[Token]:
    result: List[Token] = []
    group_index = 0
    idx = 0

    while idx < len(tokens):
        kind, value, hint = tokens[idx]

        if kind != 'code':
            result.append((kind, value, hint))
            idx += 1
            continue

        if group_index >= len(groups):
            language = guess_language_from_text(value, hint=hint)
            formatted = format_code_text(value, language)
            result.append(('code_block', formatted, language))
            idx += 1
            continue

        group = groups[group_index]
        group_index += 1

        language_hint = hint or ''
        trailing_whitespace = ''
        consumed_code = 0

        while idx < len(tokens) and consumed_code < len(group.texts):
            tk_kind, tk_value, tk_hint = tokens[idx]
            if tk_kind == 'code':
                if tk_hint and not language_hint:
                    language_hint = tk_hint
                consumed_code += 1
                idx += 1
                while idx < len(tokens) and tokens[idx][0] == 'text' and tokens[idx][1].strip() == '':
                    trailing_whitespace += tokens[idx][1]
                    idx += 1
                continue

            if tk_kind == 'text' and tk_value.strip() == '':
                trailing_whitespace += tk_value
                idx += 1
                continue

            break

        combined = '\n'.join(segment.strip('\n') for segment in group.texts if segment)
        if not combined:
            combined = value.strip('\n')

        language = guess_language_from_text(combined, hint=language_hint, code_label=group.label)
        formatted = format_code_text(combined, language)
        result.append(('code_block', formatted, language))

        if trailing_whitespace:
            result.append(('text', trailing_whitespace, None))

    while idx < len(tokens):
        result.append(tokens[idx])
        idx += 1

    return result


def tokens_to_markdown(tokens: Sequence[Token]) -> str:
    parts: List[str] = []
    for kind, value, meta in tokens:
        if kind == 'text':
            parts.append(normalize_text_segment(value))
        elif kind == 'code_block':
            lang = (meta or '').strip()
            header = f'```{lang}' if lang else '```'
            parts.append(f'{header}\n{value.rstrip()}\n```\n\n')
    markdown = ''.join(parts)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    return markdown.strip() + '\n'


def enhance_code_blocks(raw_markdown: str, document: DoclingDocument) -> str:
    tokens = split_markdown_tokens(raw_markdown)
    if not tokens:
        return raw_markdown

    groups = extract_code_groups(document)
    if not groups:
        return raw_markdown

    merged_tokens = merge_code_tokens(tokens, groups)
    return tokens_to_markdown(merged_tokens)


@lru_cache(maxsize=1)
def get_converter():
    from docling.document_converter import DocumentConverter
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
    return DocumentConverter()


def simple_pdf_to_markdown(pdf_path: Path) -> str:
    """Convert PDF to markdown using Docling with enhanced code blocks."""

    try:
        converter = get_converter()
    except ImportError as exc:
        return (
            f"# {pdf_path.stem}\n\n"
            f"*Error: docling libraries not available. Install with `pdm install`.*\n"
            f"*Import error: {exc}*\n"
        )
    try:
        result = converter.convert(str(pdf_path))
        raw_markdown = result.document.export_to_markdown()
        return enhance_code_blocks(raw_markdown, result.document)
    except Exception as exc:
        return f"# {pdf_path.stem}\n\n*Error converting PDF: {exc}*\n"


def convert_single_pdf(pdf_path: str) -> bool:
    """Convert a single PDF file to markdown."""

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"Error: File {pdf_path} does not exist")
        return False

    if pdf_file.suffix.lower() != '.pdf':
        print(f"Error: File {pdf_path} is not a PDF file")
        return False

    try:
        print(f"Converting: {pdf_file.name}")
        markdown_content = simple_pdf_to_markdown(pdf_file)
        md_file = pdf_file.with_suffix('.md')
        md_file.write_text(markdown_content, encoding='utf-8')
        print(f"✓ Created: {md_file}")
        return True
    except Exception as exc:  # pragma: no cover - defensive
        print(f"✗ Error converting {pdf_file.name}: {exc}")
        return False


def convert_directory_pdfs(directory_path: str) -> Tuple[int, int]:
    """Convert all PDFs in a directory (recursively)."""

    dir_path = Path(directory_path)

    if not dir_path.exists():
        print(f"Error: Directory {directory_path} does not exist")
        return 0, 0

    if not dir_path.is_dir():
        print(f"Error: {directory_path} is not a directory")
        return 0, 0

    pdf_files = list(dir_path.rglob('*.pdf'))
    if not pdf_files:
        print(f"No PDF files found in {directory_path}")
        return 0, 0

    print(f"Found {len(pdf_files)} PDF files in {directory_path}:")
    for pdf in pdf_files:
        print(f"  - {pdf.relative_to(dir_path)}")

    print('\nStarting conversion...')
    print('-' * 50)

    successful = 0
    failed = 0

    for pdf_file in pdf_files:
        try:
            print(f"Converting: {pdf_file.relative_to(dir_path)}")
            markdown_content = simple_pdf_to_markdown(pdf_file)
            md_file = pdf_file.with_suffix('.md')
            md_file.write_text(markdown_content, encoding='utf-8')
            print(f"✓ Created: {md_file.relative_to(dir_path)}")
            successful += 1
        except Exception as exc:  # pragma: no cover - defensive
            print(f"✗ Error converting {pdf_file.name}: {exc}")
            failed += 1

    print('-' * 50)
    print("Conversion complete:")
    print(f"  ✓ Successful: {successful}")
    print(f"  ✗ Failed: {failed}")

    return successful, failed


def convert_all_pdfs() -> Tuple[int, int]:
    """Convert all PDFs inside the base_de_conocimiento folder."""

    if BASE_DE_CONOCIMIENTO is not None:
        base_path = BASE_DE_CONOCIMIENTO
    else:
        # Fallback: resolve at runtime from script location
        script_dir = Path(__file__).parent
        base_path = script_dir.parent.parent.parent / 'base_de_conocimiento'

    if not base_path.exists():
        print(f"Error: Base path {base_path} does not exist")
        return 0, 0

    return convert_directory_pdfs(str(base_path))


def main() -> None:
    """Entrypoint for the pdf2md CLI."""

    parser = argparse.ArgumentParser(
        description="Convert PDF files to Markdown using Docling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simple_converter.py                    # Convert all PDFs in base_de_conocimiento
  python simple_converter.py -f document.pdf   # Convert single file
  python simple_converter.py -d /path/to/dir   # Convert all PDFs in directory
        """,
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', help='Convert a single PDF file')
    group.add_argument('-d', '--directory', help='Convert all PDFs in specified directory (includes subdirectories)')

    args = parser.parse_args()

    if args.file:
        success = convert_single_pdf(args.file)
        sys.exit(0 if success else 1)

    if args.directory:
        successful, failed = convert_directory_pdfs(args.directory)
        sys.exit(0 if failed == 0 else 1)

    successful, failed = convert_all_pdfs()
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()

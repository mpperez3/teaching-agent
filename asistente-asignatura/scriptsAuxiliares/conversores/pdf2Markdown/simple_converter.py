#!/usr/bin/env python3
"""
PDF to Markdown converter using Docling
Converts PDF files to Markdown format with multiple modes:
- Single file conversion
- Directory conversion (with subdirectories)
- Default: all PDFs in base_de_conocimiento directory

Features:
- Automatic code block detection and formatting
- Support for multiple programming languages (Java, Python, C++, etc.)
- Improved markdown formatting for code snippets
"""

import sys
import re
import textwrap
from pathlib import Path
import argparse

def detect_and_format_code(markdown_content):
    """
    Detect code blocks in markdown content and improve their formatting
    """
    
    # Patterns to detect code blocks and keywords for different languages
    code_patterns = {
        'java': {
            'keywords': ['public class', 'private', 'protected', 'public static void main', 'import java', 
                        'extends', 'implements', 'interface', 'enum', 'package', '@Override', 'ArrayList', 
                        'HashMap', 'String[]', 'System.out.println', 'new ArrayList', 'new HashMap'],
            'extensions': ['.java'],
            'indicators': ['class ', 'interface ', 'enum ', 'package ', 'import java.']
        },
        'python': {
            'keywords': ['def ', 'class ', 'import ', 'from ', 'if __name__', 'print(', 'input(', 
                        'len(', 'range(', 'for ', 'while ', 'try:', 'except:', 'finally:', 'with ',
                        'lambda ', 'yield ', 'return ', 'elif ', 'pass', 'break', 'continue'],
            'extensions': ['.py'],
            'indicators': ['def ', 'class ', 'import ', 'from ', 'if __name__']
        },
        'cpp': {
            'keywords': ['#include', 'using namespace', 'int main(', 'class ', 'struct ', 'cout <<', 
                        'cin >>', 'std::', 'vector<', 'string', 'iostream', 'algorithm'],
            'extensions': ['.cpp', '.h', '.hpp'],
            'indicators': ['#include', 'using namespace', 'int main(', 'std::']
        },
        'c': {
            'keywords': ['#include', 'int main(', 'printf(', 'scanf(', 'malloc(', 'free(', 'struct ',
                        'typedef', 'sizeof(', 'NULL', 'stdio.h', 'stdlib.h'],
            'extensions': ['.c', '.h'],
            'indicators': ['#include', 'int main(', 'printf(', 'scanf(']
        },
        'javascript': {
            'keywords': ['function ', 'var ', 'let ', 'const ', 'console.log', 'document.', 'window.',
                        'addEventListener', 'querySelector', 'getElementById', '=>', 'async ', 'await '],
            'extensions': ['.js'],
            'indicators': ['function ', 'console.log', 'document.', '=>']
        },
        'sql': {
            'keywords': ['SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'CREATE TABLE',
                        'DROP TABLE', 'ALTER TABLE', 'JOIN', 'INNER JOIN', 'LEFT JOIN'],
            'extensions': ['.sql'],
            'indicators': ['SELECT ', 'FROM ', 'INSERT ', 'UPDATE ', 'DELETE ', 'CREATE TABLE']
        }
    }
    
    def detect_language(text_block):
        """Detect the programming language of a text block"""
        text_lower = text_block.lower()
        scores = {}
        
        for lang, patterns in code_patterns.items():
            score = 0
            # Check for strong indicators first
            for indicator in patterns['indicators']:
                if indicator.lower() in text_lower:
                    score += 10

            # Check for keywords
            for keyword in patterns['keywords']:
                if keyword.lower() in text_lower:
                    score += 1

            scores[lang] = score
        
        # Return language with highest score, or None if no significant match
        max_score = max(scores.values()) if scores else 0
        if max_score >= 3:  # Minimum threshold for language detection
            return max(scores, key=scores.get)
        return None
    
    def is_likely_code(text):
        """Determine if a text block is likely to contain code"""
        # Check for common code indicators
        code_indicators = [
            r'\{[^}]*\}',  # Curly braces
            r'\([^)]*\)[^a-zA-Z]',  # Function calls
            r'[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^=]',  # Variable assignments
            r'//.*|/\*.*\*/',  # Comments
            r'#.*',  # Hash comments (Python, C preprocessor)
            r'public\s+class\s+\w+',  # Java class declaration
            r'def\s+\w+\s*\(',  # Python function definition
            r'#include\s*<.*>',  # C/C++ includes
            r'console\.log\s*\(',  # JavaScript console.log
            r'System\.out\.println\s*\(',  # Java print
            r'print\s*\(',  # Python print
            r'SELECT\s+.*\s+FROM',  # SQL select
        ]
        
        # Count matches
        matches = sum(1 for pattern in code_indicators if re.search(pattern, text, re.IGNORECASE))

        # Also check for indentation patterns (common in code)
        lines = text.split('\n')
        indented_lines = sum(1 for line in lines if line.startswith('    ') or line.startswith('\t'))

        return matches >= 2 or (matches >= 1 and indented_lines > len(lines) * 0.3)

    # Process the markdown content
    lines = markdown_content.split('\n')
    processed_lines = []
    i = 0

    def normalize_block(block):
        """Normalize indentation within a detected code block."""
        stripped_block = [line.rstrip('\r') for line in block]
        indents = []
        for line in stripped_block:
            if not line.strip():
                continue
            leading_spaces = len(line) - len(line.lstrip(' '))
            leading_tabs = len(line) - len(line.lstrip('\t'))
            if leading_tabs:
                indents.append(0)
            else:
                indents.append(leading_spaces)
        if indents:
            min_indent = min(indents)
            normalized = [line[min_indent:] if len(line) >= min_indent else line for line in stripped_block]
        else:
            normalized = stripped_block
        # Dedent text to remove accidental leading indentation while preserving structure
        dedented = textwrap.dedent('\n'.join(normalized)).split('\n')
        return [line.rstrip() for line in dedented]

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Preserve existing fenced code blocks without modifications
        if stripped.startswith('```'):
            processed_lines.append(line)
            i += 1
            while i < len(lines):
                processed_lines.append(lines[i])
                if lines[i].strip().startswith('```'):
                    i += 1
                    break
                i += 1
            continue

        # Check if we're starting a potential code block
        if stripped and not stripped.startswith('#') and not stripped.startswith('*') and not stripped.startswith('-') and not stripped.startswith('>'):
            block_lines = []
            j = i

            # Collect consecutive non-empty lines that might be code, stopping at existing markdown constructs
            while j < len(lines):
                candidate = lines[j]
                candidate_stripped = candidate.strip()
                if not candidate_stripped:
                    break
                if candidate_stripped.startswith('```'):
                    block_lines = []
                    break
                if candidate_stripped.startswith('#'):
                    break
                block_lines.append(candidate)
                j += 1

            if len(block_lines) >= 2:
                block_text = '\n'.join(block_lines)

                if is_likely_code(block_text):
                    detected_lang = detect_language(block_text)
                    lang_tag = detected_lang if detected_lang else ''
                    normalized_block = normalize_block(block_lines)

                    if processed_lines and processed_lines[-1].strip():
                        processed_lines.append('')

                    processed_lines.append(f'```{lang_tag}')
                    processed_lines.extend(normalized_block)
                    processed_lines.append('```')
                    processed_lines.append('')

                    i = j
                    continue

        processed_lines.append(line.rstrip())
        i += 1

    return '\n'.join(processed_lines)

def simple_pdf_to_markdown(pdf_path):
    """Convert PDF to markdown using docling with code formatting"""
    try:
        from docling.document_converter import DocumentConverter

        # Initialize the document converter
        converter = DocumentConverter()

        # Convert PDF using docling
        result = converter.convert(str(pdf_path))

        # Export to markdown
        raw_markdown = result.document.export_to_markdown()
        
        # Apply code detection and formatting
        formatted_markdown = detect_and_format_code(raw_markdown)

        return formatted_markdown

    except ImportError as e:
        return f"# {pdf_path.stem}\n\n*Error: docling libraries not available. Please install with: pip install docling*\n*Import error: {str(e)}*\n"
    except Exception as e:
        return f"# {pdf_path.stem}\n\n*Error converting PDF: {str(e)}*\n"

def convert_single_pdf(pdf_path):
    """Convert a single PDF file to markdown"""
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"Error: File {pdf_path} does not exist")
        return False

    if pdf_file.suffix.lower() != '.pdf':
        print(f"Error: File {pdf_path} is not a PDF file")
        return False

    try:
        print(f"Converting: {pdf_file.name}")

        # Generate markdown content
        markdown_content = simple_pdf_to_markdown(pdf_file)

        # Write to .md file in same directory
        md_file = pdf_file.with_suffix(".md")

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"✓ Created: {md_file}")
        return True

    except Exception as e:
        print(f"✗ Error converting {pdf_file.name}: {str(e)}")
        return False

def convert_directory_pdfs(directory_path):
    """Convert all PDFs in specified directory and subdirectories"""
    dir_path = Path(directory_path)

    if not dir_path.exists():
        print(f"Error: Directory {directory_path} does not exist")
        return 0, 0

    if not dir_path.is_dir():
        print(f"Error: {directory_path} is not a directory")
        return 0, 0

    # Find all PDF files
    pdf_files = list(dir_path.rglob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {directory_path}")
        return 0, 0

    print(f"Found {len(pdf_files)} PDF files in {directory_path}:")
    for pdf in pdf_files:
        print(f"  - {pdf.relative_to(dir_path)}")

    print("\nStarting conversion...")
    print("-" * 50)
    
    successful = 0
    failed = 0
    
    for pdf_file in pdf_files:
        try:
            print(f"Converting: {pdf_file.relative_to(dir_path)}")

            # Generate markdown content
            markdown_content = simple_pdf_to_markdown(pdf_file)

            # Write to .md file in same directory
            md_file = pdf_file.with_suffix(".md")
            
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            
            print(f"✓ Created: {md_file.relative_to(dir_path)}")
            successful += 1
            
        except Exception as e:
            print(f"✗ Error converting {pdf_file.name}: {str(e)}")
            failed += 1
    
    print("-" * 50)
    print(f"Conversion complete:")
    print(f"  ✓ Successful: {successful}")
    print(f"  ✗ Failed: {failed}")
    
    return successful, failed

def convert_all_pdfs():
    """Convert all PDFs in base_de_conocimiento directory"""

    # Find base_de_conocimiento directory
    script_dir = Path(__file__).parent
    base_path = script_dir.parent.parent.parent / "base_de_conocimiento"

    if not base_path.exists():
        print(f"Error: Base path {base_path} does not exist")
        return

    return convert_directory_pdfs(base_path)

def main():
    """Entry point function for the pdf2md command"""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to Markdown using Docling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simple_converter.py                    # Convert all PDFs in base_de_conocimiento
  python simple_converter.py -f document.pdf   # Convert single file
  python simple_converter.py -d /path/to/dir   # Convert all PDFs in directory
        """
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file',
                      help='Convert a single PDF file')
    group.add_argument('-d', '--directory',
                      help='Convert all PDF files in specified directory (includes subdirectories)')

    args = parser.parse_args()

    if args.file:
        # Convert single file
        success = convert_single_pdf(args.file)
        sys.exit(0 if success else 1)
    elif args.directory:
        # Convert directory
        successful, failed = convert_directory_pdfs(args.directory)
        sys.exit(0 if failed == 0 else 1)
    else:
        # Default: convert all PDFs in base_de_conocimiento
        successful, failed = convert_all_pdfs()
        sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
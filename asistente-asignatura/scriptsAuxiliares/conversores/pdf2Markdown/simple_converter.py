#!/usr/bin/env python3
"""
PDF to Markdown converter using Docling
Converts PDF files to Markdown format with multiple modes:
- Single file conversion
- Directory conversion (with subdirectories)
- Default: all PDFs in base_de_conocimiento directory
"""

import sys
from pathlib import Path
import argparse

def simple_pdf_to_markdown(pdf_path):
    """Convert PDF to markdown using docling"""
    try:
        from docling.document_converter import DocumentConverter

        # Initialize the document converter
        converter = DocumentConverter()

        # Convert PDF using docling
        result = converter.convert(str(pdf_path))

        # Export to markdown
        markdown_content = result.document.export_to_markdown()

        return markdown_content

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

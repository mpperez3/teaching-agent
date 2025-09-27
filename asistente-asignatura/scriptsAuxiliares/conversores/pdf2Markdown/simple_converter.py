#!/usr/bin/env python3
"""
Simple PDF to Markdown converter using pymupdf (fitz)
This is a fallback converter that works without docling if there are dependency issues
"""

import sys
from pathlib import Path
import argparse

def simple_pdf_to_markdown(pdf_path):
    """Convert PDF to markdown using pymupdf as fallback"""
    try:
        import fitz  # pymupdf
        
        # Open PDF
        doc = fitz.open(pdf_path)
        
        markdown_content = []
        markdown_content.append(f"# {pdf_path.stem}\n")
        markdown_content.append(f"*Converted from: {pdf_path.name}*\n\n")
        
        # Extract text from each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            
            if text.strip():
                markdown_content.append(f"## Page {page_num + 1}\n")
                markdown_content.append(text)
                markdown_content.append("\n---\n")
        
        doc.close()
        return "\n".join(markdown_content)
        
    except ImportError:
        return f"# {pdf_path.stem}\n\n*Error: pymupdf not available. Please install with: pip install pymupdf*\n"
    except Exception as e:
        return f"# {pdf_path.stem}\n\n*Error converting PDF: {str(e)}*\n"

def convert_all_pdfs():
    """Convert all PDFs in base_de_conocimiento directory"""
    
    # Find base_de_conocimiento directory
    script_dir = Path(__file__).parent
    base_path = script_dir.parent.parent.parent / "base_de_conocimiento"
    
    if not base_path.exists():
        print(f"Error: Base path {base_path} does not exist")
        return
    
    # Find all PDF files
    pdf_files = list(base_path.rglob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in base_de_conocimiento directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files to convert:")
    for pdf in pdf_files:
        print(f"  - {pdf.relative_to(base_path)}")
    
    print("\nStarting conversion...")
    print("-" * 50)
    
    successful = 0
    failed = 0
    
    for pdf_file in pdf_files:
        try:
            print(f"Converting: {pdf_file.relative_to(base_path)}")
            
            # Generate markdown content
            markdown_content = simple_pdf_to_markdown(pdf_file)
            
            # Write to .md file in same directory
            md_file = pdf_file.with_suffix(".md")
            
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            
            print(f"✓ Created: {md_file.relative_to(base_path)}")
            successful += 1
            
        except Exception as e:
            print(f"✗ Error converting {pdf_file.name}: {str(e)}")
            failed += 1
    
    print("-" * 50)
    print(f"Conversion complete:")
    print(f"  ✓ Successful: {successful}")
    print(f"  ✗ Failed: {failed}")
    
    return successful, failed

def main():
    """Entry point function for the pdf2md command"""
    convert_all_pdfs()

if __name__ == "__main__":
    main()

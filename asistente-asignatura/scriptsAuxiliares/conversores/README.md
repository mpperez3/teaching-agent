# Converters

This directory contains various conversion utilities for the teaching assistant project. Each converter is designed as an independent tool with its own Python environment and dependencies.

## Documentation Requirements

**All converters must be documented in this README file** with the following information:
- **Purpose**: Clear description of what the converter does
- **Use cases**: When and why to use this converter
- **Usage examples**: Command-line examples with common scenarios
- **Input/Output**: Supported file formats and expected results

## Structure

Each converter subdirectory contains:
- A complete Python project with its own `pyproject.toml`
- An isolated virtual environment (`.venv/`)
- A shell script for easy execution (`run_*.sh`)
- Documentation section in this README

## Available Converters

### markdown2Pdf/
**Purpose**: Converts Markdown files to PDF format using ReportLab for creating professional educational materials and documents.

**Use cases**:
- Generate PDF versions of exercise statements for distribution
- Create printable study materials from Markdown content
- Produce formal documentation from Markdown notes

**Usage examples**:
```bash
cd markdown2Pdf/
# Convert single Markdown file to PDF
./run_md2pdf.sh convert -f input_file.md

# Convert all Markdown files in a directory
./run_md2pdf.sh convert -d /path/to/markdown/files

# Convert with custom styling options
./run_md2pdf.sh convert -f document.md --style academic
```

**Input/Output**: 
- Input: `.md` (Markdown files)
- Output: `.pdf` (Formatted PDF documents)

---

### pdf2Markdown/
**Purpose**: Extracts and converts PDF content to Markdown format with intelligent code block detection for analysis and content processing.

**Use cases**:
- Convert PDF study materials to editable Markdown format
- Extract content from academic papers for integration into knowledge base
- Process programming exercise PDFs with proper code formatting
- Prepare PDF content for digital analysis and search

**Usage examples**:
```bash
cd pdf2Markdown/
# Convert single PDF file
./run_pdf2md.sh -f document.pdf

# Convert all PDFs in directory and subdirectories
./run_pdf2md.sh -d /path/to/pdf/files

# Convert with specific default language for code blocks
./run_pdf2md.sh -f programming_exercise.pdf -l java

# Convert all files in base_de_conocimiento (default mode)
./run_pdf2md.sh convert
```

**Input/Output**:
- Input: `.pdf` (PDF documents)
- Output: `.md` (Markdown files with formatted code blocks)

**Special features**:
- Automatic programming language detection (Java, Python, C++, C, JavaScript, SQL)
- Code block formatting with syntax highlighting
- Option to set default language to avoid auto-detection
- Improved handling of nested code structures

---

## Usage Guidelines

### Environment Setup
Each converter manages its own virtual environment automatically. The shell scripts handle:
- Virtual environment creation and activation
- Dependency installation
- Proper execution context

### Execution
Always run converters using their provided shell scripts:

```bash
# General pattern
cd [converter_name]/
./run_[converter].sh [options]
```

### Adding New Converters
When creating a new converter:

1. Create subdirectory with converter name
2. Set up isolated Python environment and dependencies
3. Create `run_[name].sh` script for execution
4. **Document the converter in this README** following the template:
   ```markdown
   ### converter_name/
   **Purpose**: [Clear description]
   **Use cases**: [When to use it]
   **Usage examples**: [Command examples]
   **Input/Output**: [Supported formats]
   ```

### Development Notes
- **Never** examine the internal code of these converters
- Each converter is self-contained and independent
- Use only the provided shell script interfaces
- Dependencies are automatically managed per project
- Virtual environments are isolated to prevent conflicts

## Important
These tools are utilities only - they are not part of the main educational content and should be treated as black-box conversion tools. Focus on using their functionality rather than understanding their implementation.

All converters must maintain this documentation standard for consistency and ease of use.

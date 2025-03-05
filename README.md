# PDF to Accessible HTML Converter

This repository contains two Python scripts that work together to convert PDFs into accessible HTML with proper math rendering and image descriptions.

## Overview

The conversion process happens in two steps:

1. **PDF to Markdown conversion** (using Agentic Document Extraction API)
2. **Markdown to Accessible HTML conversion** (with MathJax support and image descriptions)

## Prerequisites

- Python 3.7 or later
- Pip (Python package installer)
- An API key from Landing AI's Agentic Document Extraction service

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/unicef/pdf-accessible-html-converter
   cd pdf-accessible-html-converter
   ```

2. Install the required dependencies:
   ```bash
   pip install pypandoc panflute beautifulsoup4 requests
   ```

3. Install Pandoc (required by pypandoc):
   - For macOS:
     ```bash
     brew install pandoc
     ```
   - For Ubuntu/Debian:
     ```bash
     sudo apt-get install pandoc
     ```
   - For Windows:
     - Download from [pandoc.org/installing.html](https://pandoc.org/installing.html)

## Setting up the Agentic API Key

1. Obtain an API key from [Landing AI's Agentic Document Extraction service](https://landing.ai/agentic-document-extraction)

2. Set the API key as an environment variable:
   
   - For macOS/Linux:
     ```bash
     export AGENTIC_API_KEY=your_api_key_here
     ```
     
   - For Windows Command Prompt:
     ```cmd
     set AGENTIC_API_KEY=your_api_key_here
     ```
     
   - For Windows PowerShell:
     ```powershell
     $env:AGENTIC_API_KEY = "your_api_key_here"
     ```

3. To make the API key persistent, add it to your shell configuration file (`.bashrc`, `.zshrc`, etc.)

## Usage

### Step 1: Convert PDF to Markdown

```bash
python pdf-markdown.py path/to/your/document.pdf output_markdown.md
```

This step uses the Agentic Document Extraction API to convert the PDF into markdown format with properly extracted text and structure.

### Step 2: Convert Markdown to Accessible HTML

```bash
python markdown-html.py output_markdown.md final_output.html
```

This step performs several important accessibility enhancements:

- Converts figure descriptions to accessible images with alt text
- Removes redundant "Text" headings
- Properly renders mathematical expressions using MathJax
- Maintains proper table structure
- Handles special cases like currency symbols

## Features

### PDF to Markdown Converter (`pdf-markdown.py`)

- Extracts text content while maintaining document structure
- Preserves mathematical expressions
- Identifies and extracts figure descriptions
- Maintains table layouts

### Markdown to Accessible HTML Converter (`markdown-html.py`)

- **Accessibility Features**:
  - Converts figure descriptions to images with detailed alt text
  - Removes redundant "Text" headings for cleaner output
  - Maintains proper document structure

- **Math Rendering**:
  - Uses MathJax for high-quality math rendering
  - Properly handles complex math expressions, including fractions and equations
  - Preserves equation numbering in tables
  - Differentiates between math expressions and currency symbols

## Troubleshooting

### API Key Issues

If you encounter an error like:
```
Missing user record with apikey or user id: -1
```

Make sure your API key is:
1. Correctly formatted
2. Properly set in your environment
3. Active and valid

You can verify your API key is set correctly by running:
```bash
echo $AGENTIC_API_KEY  # macOS/Linux
```

### Pandoc Installation Issues

If you encounter errors related to pypandoc not finding pandoc:

1. Make sure pandoc is installed
2. Ensure it's in your system PATH
3. You can verify with:
   ```bash
   pandoc --version
   ```

### Math Rendering Issues

If mathematical expressions aren't rendering correctly:

1. Make sure MathJax is properly loading (check browser console)
2. Verify that the HTML is using proper delimiters ($, $$, etc.)
3. Check for conflicts with currency symbols

## License

[MIT License](LICENSE)

## Acknowledgments

- [Landing AI](https://landing.ai/) for the Agentic Document Extraction API
- [Pandoc](https://pandoc.org/) for document conversion
- [MathJax](https://www.mathjax.org/) for math rendering
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML processing

---

Feel free to contribute to this project by submitting issues or pull requests!

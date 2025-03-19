# PDF to Accessible HTML Converter

This repository contains two Python scripts that work together to convert PDFs into accessible HTML with proper math rendering and image descriptions.

## Overview

The conversion process happens in two steps:

1. **PDF to Markdown conversion** (using Agentic Document Extraction API)
2. **Markdown to Accessible HTML conversion** (with MathJax support and image descriptions)

## Alternative Method

There is a set of alternative scripts that use Mistral's API to convert from PDF -> JSON - > Markdown -> HTML. The Mistral API is $1 per 1000 pages, however it does not seem to support generating image descriptions out of the box. More work will be needed to prepare these scripts to handle content like the Agentic Document Extraction API.

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
python agentic-pdf-markdown.py path/to/your/document.pdf output_markdown.md
```

This step uses the Agentic Document Extraction API to convert the PDF into markdown format with properly extracted text and structure.

### Step 2: Convert Markdown to Accessible HTML

```bash
python agentic-markdown-html.py output_markdown.md final_output.html
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

# Alternative Approach with Mistral
## Setting up the Mistral API Key

This tool converts PDFs into accessible HTML using Mistral AI's OCR capabilities. The process maintains mathematical formulas, extracts images, and creates properly structured HTML documents that are accessible to screen readers and other assistive technologies.

## Prerequisites

- Python 3.8 or higher
- Mistral AI API key
- Internet connection

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/username/pdf-accessible-html-converter.git
   cd pdf-accessible-html-converter
   ```

2. Install required dependencies:
   ```bash
   pip install mistralai pypandoc panflute beautifulsoup4 requests
   ```

3. Set up your Mistral API key as an environment variable:
   ```bash
   export MISTRAL_API_KEY="your-api-key-here"
   ```

## Script Overview

This suite includes three main scripts that form a conversion pipeline:

1. **mistral-pdf-json-urlonly.py** - Extract PDF content with Mistral OCR
2. **mistral-json-to-markdown.py** - Convert JSON response to Markdown
3. **mistral-markdown-html.py** - Convert Markdown to accessible HTML

## Usage

### Step 1: PDF to JSON (OCR Processing)

Process a PDF through Mistral OCR and get a structured JSON:

```bash
python3 mistral-pdf-json-urlonly.py -o output.json
```

Options:
- `-o, --output`: Specify output JSON file (default: mistral_formatted.json)
- `-m, --markdown-only`: Also extract markdown to a separate file

Note: By default, this script uses the Arxiv sample URL. Edit the script to use your own PDF URL.

### Step 2: JSON to Markdown

Extract markdown content from the OCR JSON:

```bash
python3 mistral-json-to-markdown.py output.json -o output.md
```

Options:
- `-o, --output`: Specify output markdown file (default: [json-name].md)

### Step 3: Markdown to HTML

Convert the markdown to accessible HTML:

```bash
python3 mistral-markdown-html.py output.md output.html
```

## Complete Workflow Example

```bash
# Process PDF with OCR
python3 mistral-pdf-json-urlonly.py -o research_paper.json

# Extract markdown from JSON
python3 mistral-json-to-markdown.py research_paper.json -o research_paper.md

# Convert markdown to accessible HTML
python3 mistral-markdown-html.py research_paper.md research_paper.html
```

## Using Your Own PDFs

To process your own PDFs, modify the `sample_url` variable in mistral-pdf-json-urlonly.py:

```python
# Replace this line:
sample_url = "https://arxiv.org/pdf/2201.04234"

# With your PDF URL:
sample_url = "https://example.com/your-pdf-file.pdf"
```

## Features

- **Mathematical Formula Support**: Properly renders complex mathematical formulas
- **Image Extraction**: Extracts and includes images from the original PDF
- **Accessible Structure**: Creates HTML with proper heading hierarchy and structure
- **Figure Descriptions**: Converts figure descriptions to image alt text
- **Clean Layout**: Removes extraneous content while maintaining document structure

## Troubleshooting

- **API Key Issues**: Ensure your Mistral API key is set correctly
- **URL Processing Errors**: Verify the PDF URL is publicly accessible
- **Output Format Issues**: Check if the PDF contains unusual elements that might affect conversion

## Extending the Scripts

You can modify these scripts for additional functionality:
- Add support for local PDF files
- Integrate with document management systems
- Add additional processing for specific document types

## License

[MIT License](LICENSE)

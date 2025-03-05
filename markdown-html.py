#!/usr/bin/env python3

import sys
import io
import os
import json
import re
import pypandoc
import panflute as pf
from bs4 import BeautifulSoup

def is_figure_description_heading(heading_text):
    """
    Check if the heading text is a variation of "Figure Description".
    This matches various ways that figure descriptions might be titled.
    """
    # Convert to lowercase for case-insensitive matching
    heading_lower = heading_text.lower().strip()
    
    # Skip numbered items that are likely problem statements
    if re.match(r'^[a-z0-9]\.\s+.*', heading_lower):
        return False
    
    # Skip if it's a question about a figure rather than a description of one
    if 'find' in heading_lower or 'calculate' in heading_lower or 'solve' in heading_lower:
        return False
    
    # List of common figure description heading patterns
    figure_patterns = [
        "figure description",
        "description of figure",
        "description of the figure",
        "detailed description of the figure",
        "image description",
        "description of image", 
        "description of the image",
        "document crop description",
        "description of document crop",
        "description of the document crop",
        "image details",
        "figure details",
        "visual description"
    ]
    
    # If it's an exact match for any pattern, it's definitely a figure description
    for pattern in figure_patterns:
        if heading_lower == pattern:
            return True
    
    # If it contains both "description" and either "figure" or "image", it's likely a figure description
    if "description" in heading_lower and any(word in heading_lower for word in ["figure", "image", "graphic", "diagram", "chart", "photo"]):
        # But only if it's not asking to do something with the figure
        if not any(word in heading_lower for word in ["find", "calculate", "determine", "solve"]):
            return True
    
    # Stand-alone "figure" heading can be ambiguous, so we add more checks
    if heading_lower == "figure":
        return True
    
    return False


def is_text_heading(heading_text):
    """
    Check if the heading text is exactly "Text".
    """
    return heading_text.lower().strip() == "text"


def create_html_with_mathjax(markdown_content, title="Document"):
    """
    Convert markdown content to HTML with MathJax support.
    Uses pandoc directly for better math rendering.
    """
    # Write markdown content to a temporary file
    temp_md = "temp_content.md"
    with open(temp_md, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    # Use pandoc to convert markdown to HTML with MathJax support
    html_content = pypandoc.convert_file(
        source_file=temp_md,
        to="html",
        format="markdown",
        extra_args=[
            "--standalone",
            "--mathjax",
            f"--metadata=title:{title}"
        ]
    )
    
    # Clean up temporary file
    os.remove(temp_md)
    
    return html_content


def fix_mathjax_in_html(html_content):
    """
    Fix issues with MathJax in HTML content.
    """
    # 1. Fix MathJax configuration
    mathjax_config = '''
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
  }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
'''
    
    # Remove any existing MathJax scripts from head
    html_content = re.sub(
        r'<script[^>]*mathjax[^>]*>.*?</script>\s*',
        '',
        html_content, 
        flags=re.DOTALL | re.IGNORECASE
    )
    
    # Insert our MathJax configuration before </head>
    html_content = html_content.replace('</head>', f'{mathjax_config}</head>')
    
    # 2. Fix CSS with math delimiters that might break MathJax
    # Look for CSS rules with $ signs and fix them
    def fix_css_math_delimiters(match):
        css_rule = match.group(0)
        # Replace $ in CSS with escaped versions
        fixed_css = css_rule.replace('$', '\\$')
        return fixed_css
    
    # Find and fix CSS rules with $ signs
    html_content = re.sub(
        r'<style>.*?</style>',
        lambda match: fix_css_math_delimiters(match),
        html_content,
        flags=re.DOTALL
    )
    
    # 3. Fix common math syntax issues
    
    # Fix malformed inline math in spans
    html_content = re.sub(
        r'<span class="math inline">\\\(?\$?(.*?)\\?\)?\$?</span>',
        r'<span class="math inline">$\1$</span>',
        html_content
    )
    
    # Fix malformed display math in spans
    html_content = re.sub(
        r'<span class="math display">\\\[?\$?(.*?)\\?\]?\$?</span>',
        r'<span class="math display">$$\1$$</span>',
        html_content
    )
    
    # Clean excessive backslashes and parentheses in math expressions
    html_content = re.sub(
        r'\$\\?\((.*?)\\?\)\$',
        r'$\1$',
        html_content
    )
    
    # 4. Fix tables with equations while preserving numbering
    
    # Process tables one by one
    table_pattern = r'(<table>.*?</table>)'
    tables = re.findall(table_pattern, html_content, re.DOTALL)
    
    for table in tables:
        fixed_table = table
        
        # Fix math expressions inside list items within table cells
        # This preserves the list numbering but makes the math expressions render properly
        fixed_table = re.sub(
            r'(<td>\s*<ol[^>]*>\s*<li>)\s*\(\s*([^<>]*?=.*?[^<>]*?)\s*\)(\s*</li>\s*</ol>\s*</td>)',
            r'\1$\2$\3',
            fixed_table,
            flags=re.DOTALL
        )
        
        # Fix "Does (x = 7)?" in table cells
        fixed_table = re.sub(
            r'(<td>)\s*Does\s*\(\s*([^()<>]*?)\s*\)\?(\s*</td>)',
            r'\1Does $\2$?\3',
            fixed_table
        )
        
        # Replace the original table with the fixed version
        html_content = html_content.replace(table, fixed_table)
    
    # 5. More general fixes for plain text that should be math
    
    # Fix inline equations with parentheses
    html_content = re.sub(
        r'(?<!\$)\(([^()<>]*?=.*?[^()<>]*?)\)',
        r'$\1$',
        html_content
    )
    
    # Fix fractions in math expressions
    html_content = re.sub(
        r'\$(\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\})\$',
        r'$\1$',
        html_content
    )
    
    # 6. Protect currency symbols in paragraphs
    # This is the key fix for handling dollar signs in text
    html_content = protect_currency_in_paragraphs(html_content)
    
    # 7. Add additional CSS for better math display
    math_css = '''
<style>
/* Improved math styling */
.math {
  font-family: 'STIX Two Math', 'Latin Modern Math', serif;
}
mjx-container {
  display: inline-block;
  margin: 0;
  padding: 0;
  overflow-x: auto;
  overflow-y: hidden;
  max-width: 100%;
}
.mjx-full-width {
  display: block;
  width: 100%;
  text-align: center;
}
table {
  border-collapse: collapse;
  margin: 1em 0;
  width: 100%;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
  font-weight: bold;
}
</style>
'''
    
    # Add our custom CSS
    html_content = html_content.replace('</head>', f'{math_css}</head>')
    
    return html_content


def protect_currency_in_paragraphs(html_content):
    """
    Protect currency symbols ($) in paragraphs from being interpreted as math delimiters.
    """
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all paragraphs
    paragraphs = soup.find_all('p')
    
    # Process each paragraph
    for p in paragraphs:
        # Get the HTML content of the paragraph
        html = str(p)
        
        # Skip paragraphs that already have math spans
        if '<span class="math' in html:
            continue
        
        # Find potential currency patterns
        # This pattern looks for dollar signs followed by digits, possibly with decimal points
        # But avoids matching what looks like a math expression with = signs, operators, etc.
        updated_html = re.sub(
            r'(\$)(\d+(?:\.\d+)?)',  # $15.00, $0.20, etc.
            r'<span class="currency">\1</span>\2',
            html
        )
        
        # Replace the original paragraph HTML if changes were made
        if updated_html != html:
            new_p = BeautifulSoup(updated_html, 'html.parser')
            p.replace_with(new_p)
    
    # Return the updated HTML
    return str(soup)


def process_headings_and_figures(html_content):
    """
    Process HTML content to:
    1. Remove headings with text "Text"
    2. Convert figure description sections to images with alt text
    """
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all headings
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    # Process each heading
    for heading in headings:
        heading_text = heading.get_text().strip()
        
        # Check if it's a "Text" heading to remove
        if is_text_heading(heading_text):
            print(f"Removing 'Text' heading: '{heading_text}'")
            heading.extract()
            continue
        
        # Check if it's a figure description heading
        if is_figure_description_heading(heading_text):
            print(f"Processing figure description: '{heading_text}'")
            
            # Collect alt text from subsequent elements until we hit another heading
            alt_lines = []
            elements_to_remove = []
            next_element = heading.next_sibling
            
            while next_element and not (next_element.name and next_element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                if hasattr(next_element, 'get_text'):
                    # Get text content and clean HTML comments
                    text = next_element.get_text().strip()
                    text = re.sub(r'<!--.*?-->', '', text)
                    
                    if text:
                        alt_lines.append(text)
                    
                    # Remember element to remove later
                    elements_to_remove.append(next_element)
                
                next_element = next_element.next_sibling
            
            # Join all collected text into alt text
            alt_text = " ".join(alt_lines).strip()
            
            # Create an img element with the alt text
            if alt_text:
                img_tag = soup.new_tag('img')
                img_tag['src'] = 'placeholder.png'
                img_tag['alt'] = alt_text
                
                # Create a paragraph to contain the image
                p_tag = soup.new_tag('p')
                p_tag.append(img_tag)
                
                # Replace the heading with the image
                heading.replace_with(p_tag)
                
                # Remove all the content that was converted to alt text
                for element in elements_to_remove:
                    element.extract()
    
    # Return the modified HTML
    return str(soup)


def process_markdown_file(input_md, output_html):
    """
    Process a markdown file to HTML with:
    - Text heading removal
    - Figure description conversion to images with alt text
    - Proper math rendering
    - Currency symbol protection
    """
    print(f"Processing {input_md} to {output_html}")
    
    # 1. Read markdown content
    with open(input_md, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 2. Get title from the markdown content if available
    title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Document"
    
    # 3. Convert markdown to HTML with MathJax
    html_content = create_html_with_mathjax(markdown_content, title)
    
    # 4. Process headings and figure descriptions
    html_content = process_headings_and_figures(html_content)
    
    # 5. Fix MathJax issues in the HTML
    fixed_html = fix_mathjax_in_html(html_content)
    
    # 6. Write the result to the output file
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(fixed_html)
    
    print(f"Successfully converted {input_md} to {output_html}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python markdown-html.py <input_file.md> <output_file.html>")
        sys.exit(1)

    input_md = sys.argv[1]
    output_html = sys.argv[2]
    
    process_markdown_file(input_md, output_html)


if __name__ == "__main__":
    main()
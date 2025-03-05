#!/usr/bin/env python3

import sys
import re
import argparse
from bs4 import BeautifulSoup

def fix_math_html(input_html, output_html):
    # Read the input HTML file
    with open(input_html, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Add MathJax configuration to the head
    head = soup.head
    
    # Remove any existing MathJax scripts
    for script in head.find_all('script', src=lambda x: x and 'mathjax' in x.lower()):
        script.decompose()
    
    # Create and insert MathJax configuration
    mathjax_config = soup.new_tag('script')
    mathjax_config.string = '''
    MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true,
        processEnvironments: true
      },
      options: {
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
      },
      svg: {
        fontCache: 'global'
      }
    };
    '''
    head.append(mathjax_config)
    
    # Add MathJax script
    mathjax_script = soup.new_tag('script')
    mathjax_script['id'] = 'MathJax-script'
    mathjax_script['async'] = True
    mathjax_script['src'] = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js'
    head.append(mathjax_script)
    
    # 2. Add custom styling for math elements
    style_tag = None
    for tag in head.find_all('style'):
        style_tag = tag
        break
    
    if style_tag:
        # Add additional CSS to existing style tag
        style_tag.string += '''
        /* Math styling */
        .math {
          font-family: 'Latin Modern Math', 'STIX Two Math', serif;
        }
        mjx-container {
          overflow-x: auto;
          overflow-y: hidden;
          max-width: 100%;
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
        '''
    
    # 3. Fix math expressions in the document
    
    # Function to clean and fix math expressions
    def fix_math_expression(match):
        expr = match.group(1)
        # Clean up the expression - remove redundant escapes, fix common issues
        expr = expr.replace('\\\\', '\\')  # Fix double escapes
        
        # Fix specific math notations
        expr = re.sub(r'\\frac\s*\{([^}]+)\}\s*\{([^}]+)\}', r'\\frac{\1}{\2}', expr)
        
        return f'${expr}$'
    
    # 4. Fix span elements with class="math inline"
    for span in soup.find_all('span', class_='math'):
        # Get the text content
        content = span.get_text()
        
        # Check if this is already properly formatted
        if content.startswith('$') and content.endswith('$'):
            continue
            
        # Clean the math expression
        content = content.replace('(', '').replace(')', '')
        
        # Replace the span with proper math syntax
        new_tag = soup.new_tag('span', attrs={'class': 'math inline'})
        new_tag.string = f'${content}$'
        span.replace_with(new_tag)
    
    # 5. Fix math formulas in table cells
    for td in soup.find_all('td'):
        text = td.get_text()
        # Look for text with math-like patterns
        if '\\' in text or '$' in text or '(' in text and ')' in text:
            # This is a potential math expression that needs fixing
            math_fixed = re.sub(r'\(\s*([^)]*?)\s*\)', r'$\1$', text)
            td.clear()
            td.append(math_fixed)
    
    # 6. Write the fixed HTML to output file
    with open(output_html, 'w', encoding='utf-8') as out_file:
        out_file.write(str(soup))
    
    print(f"Fixed HTML saved to: {output_html}")

def main():
    parser = argparse.ArgumentParser(description="Fix math expressions in HTML files for proper rendering with MathJax")
    parser.add_argument("input_html", help="Path to the input HTML file")
    parser.add_argument("-o", "--output", help="Path to the output HTML file (default: fixed_[input].html)")
    
    args = parser.parse_args()
    
    # Set output path if not provided
    output_html = args.output
    if not output_html:
        # Extract filename and add "fixed_" prefix
        filename = args.input_html.split('/')[-1]
        output_html = f"fixed_{filename}"
    
    fix_math_html(args.input_html, output_html)

if __name__ == "__main__":
    main()

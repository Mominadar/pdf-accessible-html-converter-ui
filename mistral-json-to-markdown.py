#!/usr/bin/env python3

import json
import argparse
from pathlib import Path

def extract_markdown_from_json(json_file, output_file):
    """
    Extract markdown content from a JSON file and write it to a markdown file.
    
    Args:
        json_file (str): Path to the JSON file
        output_file (str): Path to the output markdown file
    """
    try:
        # Read the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract markdown content from each page
        markdown_content = ""
        if 'pages' in data:
            for page in data['pages']:
                if 'markdown' in page:
                    markdown_content += page['markdown'] + "\n\n"
        
        # Write the markdown content to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        print(f"Successfully extracted markdown to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract markdown from JSON and save to a file')
    parser.add_argument('json_file', help='Path to the JSON file')
    parser.add_argument('-o', '--output', help='Output markdown file path (default: input filename with .md extension)')
    args = parser.parse_args()
    
    json_file = args.json_file
    
    # If output file is not specified, use the JSON filename with .md extension
    if args.output:
        output_file = args.output
    else:
        output_file = Path(json_file).stem + ".md"
    
    extract_markdown_from_json(json_file, output_file)

if __name__ == "__main__":
    main()
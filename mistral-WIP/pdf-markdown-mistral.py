#!/usr/bin/env python3

import os
import sys
import argparse
import time
from mistralai import Mistral
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Convert PDF to accessible markdown using Mistral OCR")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output file path (default: input filename with .md extension)")
    parser.add_argument("-f", "--format", choices=["markdown", "html"], default="markdown", 
                        help="Output format (default: markdown)")
    parser.add_argument("-m", "--model", default="mistral-ocr-latest",
                        help="Mistral OCR model to use (default: mistral-ocr-latest)")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Check for API key
    if "MISTRAL_API_KEY" not in os.environ:
        print("Error: MISTRAL_API_KEY environment variable is not set.")
        print("Please set it with: export MISTRAL_API_KEY='your-api-key'")
        sys.exit(1)
    
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    
    # Determine output file path
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.pdf_path)
        extension = ".md" if args.format == "markdown" else ".html"
        output_path = str(input_path.with_suffix(extension))
    
    try:
        print(f"Processing {args.pdf_path}...")
        
        # Check if it's a local file or URL
        if args.pdf_path.startswith(('http://', 'https://')):
            # URL-based document
            document_config = {
                "type": "document_url",
                "document_url": args.pdf_path
            }
        else:
            # Local file - read it and encode with base64
            with open(args.pdf_path, "rb") as file:
                import base64
                file_content = base64.b64encode(file.read()).decode('utf-8')
                
                document_config = {
                    "type": "document_base64",
                    "document_base64": file_content
                }
        
        # Start OCR processing
        print("Starting OCR processing...")
        ocr_response = client.ocr.process(
            model=args.model,
            document=document_config
        )
        
        # Extract the content based on format
        if args.format == "markdown":
            # Combine markdown from all pages
            content = ""
            for page in ocr_response["pages"]:
                content += page["markdown"] + "\n\n"
        else:
            # HTML format
            # Note: Check if Mistral OCR API supports direct HTML output
            # If not, you might need to convert markdown to HTML
            if "html" in ocr_response["pages"][0]:
                content = ""
                for page in ocr_response["pages"]:
                    content += page["html"] + "\n"
            else:
                # Convert markdown to HTML if needed
                import markdown
                content = "<html><body>\n"
                for page in ocr_response["pages"]:
                    content += markdown.markdown(page["markdown"]) + "\n"
                content += "</body></html>"
        
        # Save output
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully saved output to {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
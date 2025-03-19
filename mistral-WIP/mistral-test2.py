#!/usr/bin/env python3

import os
import sys
import argparse
from mistralai import Mistral
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Convert online PDF to Markdown using Mistral OCR")
    parser.add_argument("pdf_url", help="URL to the PDF file")
    parser.add_argument("-o", "--output", help="Output file path (default: extracted filename with .md extension)")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Check if input is a URL
    pdf_url = args.pdf_url
    if not pdf_url.startswith(('http://', 'https://')):
        print("Error: Input must be a URL starting with http:// or https://")
        sys.exit(1)
    
    # Check for API key
    if "MISTRAL_API_KEY" not in os.environ:
        print("Error: MISTRAL_API_KEY environment variable is not set")
        print("Please set it with: export MISTRAL_API_KEY='your-api-key'")
        sys.exit(1)
    
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        filename = os.path.basename(pdf_url.split('?')[0])
        if not filename:
            filename = "downloaded_file.pdf"
        output_path = filename.replace('.pdf', '.md')
    
    try:
        print(f"Processing URL: {pdf_url}")
        print("Starting OCR processing...")
        
        # Create document config for URL processing
        document_config = {
            "type": "document_url",
            "document_url": pdf_url
        }
        
        if args.debug:
            print(f"Document config: {document_config}")
        
        # Process with the URL
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document=document_config
        )
        
        print("OCR processing completed")
        
        # Extract and save content
        content = ""
        if hasattr(ocr_response, 'pages'):
            # Object response
            for page in ocr_response.pages:
                if hasattr(page, 'markdown'):
                    content += page.markdown + "\n\n"
                    print(f"Processed page {page.index}")
        elif isinstance(ocr_response, dict) and "pages" in ocr_response:
            # Dict response
            for page in ocr_response["pages"]:
                if "markdown" in page:
                    content += page["markdown"] + "\n\n"
                    print(f"Processed page {page.get('index', 'unknown')}")
        else:
            print("Unexpected response format")
            if args.debug:
                print(f"Response type: {type(ocr_response)}")
                print(f"Response: {ocr_response}")
                
        if content:
            # Write the content to the output file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Successfully saved output to {output_path}")
        else:
            print("No markdown content found in the OCR response")
            if args.debug:
                print("Response type:", type(ocr_response))
                if hasattr(ocr_response, 'keys'):
                    print("Response keys:", ocr_response.keys())
                elif hasattr(ocr_response, '__dict__'):
                    print("Response attrs:", ocr_response.__dict__)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
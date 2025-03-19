#!/usr/bin/env python3

import os
import sys
import argparse
import json
import base64
from mistralai import Mistral
from pathlib import Path
import requests

def parse_args():
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown using Mistral OCR")
    parser.add_argument("pdf_path", help="Path to the PDF file to process or a URL")
    parser.add_argument("-o", "--output", help="Output file path (default: input filename with .md extension)")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Determine if input is a URL or local file
    is_url = args.pdf_path.startswith(('http://', 'https://'))
    
    # Validate file existence if local
    if not is_url and not Path(args.pdf_path).exists():
        print(f"Error: File {args.pdf_path} does not exist")
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
        if is_url:
            filename = os.path.basename(args.pdf_path.split('?')[0])
            if not filename.endswith('.pdf'):
                filename = "downloaded_file.pdf"
            output_path = filename.replace('.pdf', '.md')
        else:
            input_path = Path(args.pdf_path)
            output_path = str(input_path.with_suffix('.md'))
    
    try:
        print(f"Processing {'URL' if is_url else 'file'}: {args.pdf_path}...")
        print("Starting OCR processing...")
        
        if is_url:
            # Direct URL processing
            document_config = {
                "type": "document_url",
                "document_url": args.pdf_path
            }
        else:
            # Try a different approach with direct base64 encoding
            print("Using base64 encoding for direct file upload...")
            
            with open(args.pdf_path, "rb") as file:
                # Encode the file content
                file_content = base64.b64encode(file.read()).decode('utf-8')
            
            # Use document_base64 type
            document_config = {
                "type": "document_base64",
                "document_base64": file_content
            }
        
        # Make sure document_config is well-formed
        if args.debug:
            print(f"Document config type: {document_config['type']}")
        
        # Process with the URL or base64 data
        try:
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
            elif isinstance(ocr_response, dict) and "pages" in ocr_response:
                # Dict response
                for page in ocr_response["pages"]:
                    if "markdown" in page:
                        content += page["markdown"] + "\n\n"
            else:
                print("Unexpected response format")
                if args.debug:
                    print("Response:", ocr_response)
                    
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
        
        except Exception as api_error:
            print(f"Mistral API Error: {str(api_error)}")
            if args.debug and hasattr(api_error, 'response') and hasattr(api_error.response, 'text'):
                print("API Response:", api_error.response.text)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
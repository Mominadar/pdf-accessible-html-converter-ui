#!/usr/bin/env python3

import os
import sys
import argparse
import json
import re
from mistralai import Mistral
from pathlib import Path

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle special Mistral API objects"""
    def default(self, obj):
        # Check for object types that need special handling
        if obj.__class__.__name__ == "OCRImageObject":
            # Convert OCRImageObject to dict with its attributes
            result = {}
            # Common attributes for OCRImageObject
            for attr in ['id', 'width', 'height', 'alt', 'url', 'base64']:
                if hasattr(obj, attr):
                    value = getattr(obj, attr)
                    if value is not None:
                        result[attr] = value
            return result
        # Use normal JSON encoding for everything else
        return super().default(obj)

def parse_args():
    parser = argparse.ArgumentParser(description="Save properly formatted Mistral OCR response")
    parser.add_argument("-o", "--output", default="mistral_formatted.json", help="Output file path (default: mistral_formatted.json)")
    parser.add_argument("-m", "--markdown-only", action="store_true", help="Extract just markdown to a separate file")
    return parser.parse_args()

def extract_page_attributes(page_str):
    """Extract attributes from page string representation into a proper dictionary"""
    # Extract index
    index_match = re.search(r'index=(\d+)', page_str)
    index = int(index_match.group(1)) if index_match else None
    
    # Extract markdown content
    markdown_match = re.search(r'markdown="(.*?)"(?= images|\Z)', page_str, re.DOTALL)
    markdown = markdown_match.group(1) if markdown_match else ""
    
    # Extract images
    images_match = re.search(r'images=\[(.*?)\]', page_str)
    images = [] # Default empty array
    
    # Extract dimensions
    dimensions_match = re.search(r'dimensions=OCRPageDimensions\(dpi=(\d+), height=(\d+), width=(\d+)\)', page_str)
    dimensions = {}
    if dimensions_match:
        dimensions = {
            "dpi": int(dimensions_match.group(1)),
            "height": int(dimensions_match.group(2)),
            "width": int(dimensions_match.group(3))
        }
    
    return {
        "index": index,
        "markdown": markdown,
        "images": images,
        "dimensions": dimensions
    }

def main():
    args = parse_args()
    
    # Check for API key
    if "MISTRAL_API_KEY" not in os.environ:
        print("Error: MISTRAL_API_KEY environment variable is not set")
        print("Please set it with: export MISTRAL_API_KEY='your-api-key'")
        sys.exit(1)
    
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    
    output_path = args.output
    
    try:
        # Use the sample URL directly from Mistral's documentation
        sample_url = "https://arxiv.org/pdf/2201.04234"
        # sample_url = "https://pdfobject.com/pdf/sample.pdf"
        # sample_url = "https://elasticsounds.github.io/pdf-public/c4611_sample_explain.pdf"
        # sample_url = "https://elasticsounds.github.io/pdf-public/toolkit_unicef_a.pdf"
        print(f"Processing Arxiv URL: {sample_url}")
        print("Starting OCR processing...")
        
        # Process with the URL - exactly as shown in Mistral docs
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": sample_url
            },
            include_image_base64=True
        )
        
        print("OCR processing completed")
        
        # Create properly structured JSON
        structured_data = {}
        markdown_content = ""
        
        if isinstance(ocr_response, dict):
            # Handle dictionary response
            structured_data = ocr_response.copy()
            
            # Fix pages if they're string representations
            if "pages" in structured_data and isinstance(structured_data["pages"], list):
                fixed_pages = []
                for page in structured_data["pages"]:
                    if isinstance(page, str):
                        # Convert string representation to dict
                        page_dict = extract_page_attributes(page)
                        fixed_pages.append(page_dict)
                        markdown_content += page_dict["markdown"] + "\n\n"
                    else:
                        # Already a dict or object
                        fixed_pages.append(page)
                        if "markdown" in page:
                            markdown_content += page["markdown"] + "\n\n"
                structured_data["pages"] = fixed_pages
                
        elif hasattr(ocr_response, 'pages'):
            # Handle object response
            structured_data["pages"] = []
            for page in ocr_response.pages:
                page_dict = {}
                if hasattr(page, 'index'):
                    page_dict["index"] = page.index
                if hasattr(page, 'markdown'):
                    page_dict["markdown"] = page.markdown
                    markdown_content += page.markdown + "\n\n"
                if hasattr(page, 'images'):
                    page_dict["images"] = page.images
                if hasattr(page, 'dimensions'):
                    page_dict["dimensions"] = {
                        "dpi": page.dimensions.dpi if hasattr(page.dimensions, 'dpi') else None,
                        "height": page.dimensions.height if hasattr(page.dimensions, 'height') else None,
                        "width": page.dimensions.width if hasattr(page.dimensions, 'width') else None
                    }
                structured_data["pages"].append(page_dict)
        
        # Save the properly structured JSON using the custom encoder
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=2, ensure_ascii=False, cls=CustomJSONEncoder)
            
        print(f"Properly formatted JSON saved to {output_path}")
        
        # Save markdown content to a separate file if requested
        if args.markdown_only and markdown_content:
            markdown_path = output_path.replace(".json", ".md")
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Markdown content extracted to {markdown_path}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
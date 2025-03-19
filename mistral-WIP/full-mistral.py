#!/usr/bin/env python3

import os
import sys
import json
import argparse
import time
from pathlib import Path
from mistralai import Mistral
from mistralai.models.chat import ChatMessage
from mistralai import DocumentURLChunk, ImageURLChunk, TextChunk

def parse_args():
    parser = argparse.ArgumentParser(description="Process PDF with Mistral OCR and generate image alt-text")
    parser.add_argument("pdf_url", help="URL to the PDF file")
    parser.add_argument("-o", "--output", default="output", help="Base name for output files (without extension)")
    parser.add_argument("--no-alt-text", action="store_true", help="Skip alt-text generation for images")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    return parser.parse_args()

def generate_alt_text(client, base64_image, retry_count=3, sleep_time=2):
    """Generate alt-text for an image using Pixtral"""
    base64_data_url = f"data:image/jpeg;base64,{base64_image}"
    
    for attempt in range(retry_count):
        try:
            response = client.chat.complete(
                model="pixtral-12b-latest",  # Using vision model
                messages=[
                    ChatMessage(
                        role="user",
                        content=[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": base64_data_url
                                }
                            },
                            {
                                "type": "text", 
                                "text": "Generate a detailed alt-text description for this image. Focus on describing the visual content clearly and concisely in 2-3 sentences. Explain what the image shows, including any charts, diagrams, or figures. If it contains data visualizations, summarize what they represent."
                            }
                        ]
                    )
                ],
                temperature=0.1,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt < retry_count - 1:
                print(f"Error generating alt-text (attempt {attempt+1}/{retry_count}): {str(e)}")
                time.sleep(sleep_time)
            else:
                return f"Image description unavailable due to processing error: {str(e)}"

def main():
    args = parse_args()
    
    # Check for API key
    if "MISTRAL_API_KEY" not in os.environ:
        print("Error: MISTRAL_API_KEY environment variable is not set")
        print("Please set it with: export MISTRAL_API_KEY='your-api-key'")
        sys.exit(1)
    
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    
    # Base names for output files
    md_output_path = f"{args.output}.md"
    json_output_path = f"{args.output}.json"
    alt_text_output_path = f"{args.output}_alt_text.json"
    
    try:
        # Process PDF with OCR
        print(f"Processing PDF from URL: {args.pdf_url}")
        print("Starting OCR processing...")
        
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": args.pdf_url
            },
            include_image_base64=True  # Important to get the images
        )
        
        print("OCR processing completed")
        
        # Extract content and create structured data
        markdown_content = ""
        structured_data = {"pages": []}
        image_alt_texts = {}
        
        for page in ocr_response.pages:
            page_data = {
                "index": page.index,
                "markdown": page.markdown,
                "images": []
            }
            
            # Process images if present
            if hasattr(page, 'images') and page.images:
                print(f"Processing {len(page.images)} images on page {page.index}")
                
                for img in page.images:
                    image_id = img.id
                    image_data = {
                        "id": image_id
                    }
                    
                    # Generate alt-text if requested
                    if not args.no_alt_text and hasattr(img, 'base64'):
                        print(f"  Generating alt-text for image {image_id}")
                        alt_text = generate_alt_text(client, img.base64)
                        image_alt_texts[image_id] = alt_text
                        image_data["alt_text"] = alt_text
                    
                    page_data["images"].append(image_data)
            
            structured_data["pages"].append(page_data)
            markdown_content += page.markdown + "\n\n"
        
        # Save markdown content
        with open(md_output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Markdown content saved to {md_output_path}")
        
        # Save structured JSON
        with open(json_output_path, "w", encoding="utf-8") as f:
            json.dump(structured_data, f, indent=2)
        print(f"Structured JSON saved to {json_output_path}")
        
        # Save alt-text mapping separately
        if image_alt_texts:
            with open(alt_text_output_path, "w", encoding="utf-8") as f:
                json.dump(image_alt_texts, f, indent=2)
            print(f"Image alt-text mapping saved to {alt_text_output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
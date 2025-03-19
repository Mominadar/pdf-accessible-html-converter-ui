#!/usr/bin/env python3

import os
import sys
import json
import re
import argparse
import base64
from pathlib import Path
from mistralai import Mistral

def parse_args():
    parser = argparse.ArgumentParser(description="Generate alt-text for images using Mistral OCR")
    parser.add_argument("json_file", help="Path to the OCR JSON file with image references")
    parser.add_argument("image_dir", help="Directory containing the image files")
    parser.add_argument("-o", "--output", default="image_alt_text.json", help="Output JSON file with alt-text")
    return parser.parse_args()

def extract_image_references(json_data):
    """Extract all image IDs from the JSON data"""
    image_ids = set()
    
    if 'pages' in json_data:
        for page in json_data['pages']:
            if 'images' in page and page['images']:
                for image in page['images']:
                    if 'id' in image:
                        image_ids.add(image['id'])
    
    return list(image_ids)

def extract_figure_descriptions(json_data):
    """Extract figure descriptions from markdown content"""
    figure_descriptions = {}
    
    # Pattern to match figure descriptions (Figure X: description)
    figure_pattern = re.compile(r'Figure\s+(\d+):\s+([^\n]+)')
    
    if 'pages' in json_data:
        for page in json_data['pages']:
            if 'markdown' in page:
                markdown = page['markdown']
                matches = figure_pattern.findall(markdown)
                for match in matches:
                    figure_num = match[0]
                    description = match[1].strip()
                    figure_descriptions[f"Figure {figure_num}"] = description
    
    return figure_descriptions

def process_images_with_ocr(image_ids, image_dir):
    """Process each image with Mistral OCR to generate alt-text"""
    if "MISTRAL_API_KEY" not in os.environ:
        print("Error: MISTRAL_API_KEY environment variable is not set")
        print("Please set it with: export MISTRAL_API_KEY='your-api-key'")
        sys.exit(1)
    
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    
    alt_texts = {}
    
    for image_id in image_ids:
        image_path = Path(image_dir) / image_id
        
        if not image_path.exists():
            print(f"Warning: Image {image_id} not found in {image_dir}")
            alt_texts[image_id] = "Image description not available"
            continue
            
        try:
            print(f"Processing image: {image_id}")
            
            # Encode image to base64
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode()
                base64_data_url = f"data:image/jpeg;base64,{encoded_image}"
            
            # Process with Mistral OCR
            response = client.chat.complete(
                model="pixtral-12b-latest",  # Using vision model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": base64_data_url
                                }
                            },
                            {
                                "type": "text", 
                                "text": "Generate a detailed alt-text description for this image. Focus on describing the visual content in a way that would be helpful for someone who cannot see the image."
                            }
                        ]
                    }
                ]
            )
            
            alt_text = response.choices[0].message.content
            alt_texts[image_id] = alt_text
            
        except Exception as e:
            print(f"Error processing image {image_id}: {str(e)}")
            alt_texts[image_id] = f"Error generating description: {str(e)}"
    
    return alt_texts

def process_with_existing_descriptions(image_ids, json_data):
    """Create alt texts based on existing figure descriptions in the markdown"""
    alt_texts = {}
    figure_descriptions = extract_figure_descriptions(json_data)
    
    # Map image IDs (like img-0.jpeg) to figure numbers if possible
    for page in json_data['pages']:
        if 'markdown' in page and 'images' in page and page['images']:
            markdown = page['markdown']
            
            # Look for image references in markdown
            for image in page['images']:
                if 'id' in image:
                    image_id = image['id']
                    
                    # Try to find which figure number this image corresponds to
                    for fig_num, desc in figure_descriptions.items():
                        # Simple heuristic: if image reference is close to figure text
                        image_ref_pos = markdown.find(image_id)
                        fig_text_pos = markdown.find(fig_num)
                        
                        if image_ref_pos != -1 and fig_text_pos != -1 and abs(image_ref_pos - fig_text_pos) < 200:
                            alt_texts[image_id] = f"{fig_num}: {figure_descriptions[fig_num]}"
                            break
                    
                    # If we couldn't match to a figure, use a placeholder
                    if image_id not in alt_texts:
                        alt_texts[image_id] = f"Image {image_id} (description not found in text)"
    
    return alt_texts

def main():
    args = parse_args()
    
    # Load the JSON data
    try:
        with open(args.json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {str(e)}")
        sys.exit(1)
    
    # Extract image references
    image_ids = extract_image_references(json_data)
    print(f"Found {len(image_ids)} image references in the JSON")
    
    if len(image_ids) == 0:
        print("No images found in the JSON")
        sys.exit(0)
    
    # Check if image directory exists
    image_dir = Path(args.image_dir)
    
    if image_dir.exists() and image_dir.is_dir():
        # Process images with OCR
        alt_texts = process_images_with_ocr(image_ids, image_dir)
    else:
        print(f"Image directory not found or not a directory: {args.image_dir}")
        print("Generating alt-text from existing figure descriptions in the markdown...")
        
        # Use existing descriptions from markdown
        alt_texts = process_with_existing_descriptions(image_ids, json_data)
    
    # Save the alt-text JSON
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(alt_texts, f, indent=2)
    
    print(f"Alt-text JSON saved to {args.output}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import os
import requests
import json

API_KEY = os.environ.get("AGENTIC_API_KEY")

class AgenticPDFToMarkdownConverter:
    """
    A converter that uses the Agentic Document Extraction API to extract content from PDFs
    and save it as Markdown files.
    """
    def __init__(self):
        self.api_key = API_KEY
        # Updated URL based on the documentation
        self.base_url = "https://api.va.landing.ai/v1/tools/agentic-document-analysis"
        # Updated headers based on the documentation
        self.headers = {
            "Authorization": f"Basic {self.api_key}"
        }
     
    def extract_pdf_content(self, pdf_path, output_format="markdown"):
        """
        Send a PDF file to the API for content extraction.
        Returns the parsed content or None if failed.
        """
        print(f"Processing PDF: {pdf_path}")
        
        try:

            response = requests.get(pdf_path)
            response.raise_for_status()  # Raise error if request fails

            # Read PDF from memory
            pdf_bytes = response.content
            
            # with open(pdf_path, "rb") as pdf_file:
                # Using 'pdf' as the file parameter based on the documentation
            files = {
                "pdf": pdf_bytes
            }
            
            # Add any additional parameters you might need
            params = {
                "format": output_format
            }
            
            print(f"Sending request to: {self.base_url}")
            print(f"Authorization: Basic {self.api_key[:5]}...{self.api_key[-5:]}")
            
            # Make the API request
            response = requests.post(
                self.base_url,
                headers=self.headers,
                files=files,
                params=params
            )
            
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                # The request was successful
                return response.json()
            else:
                print(f"Request failed with status code {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error during API request: {str(e)}")
            return None
    
    def extract_markdown_from_response(self, response_data):
        """
        Extract markdown content from the API response.
        The exact structure depends on the API response format.
        """
        # Look for markdown content in common field names
        if isinstance(response_data, str):
            # If the response is already a string, return it
            return response_data
            
        if isinstance(response_data, dict):
            # Check for common field names that might contain the content
            for field in ['markdown', 'content', 'text', 'result', 'data']:
                if field in response_data:
                    content = response_data[field]
                    if isinstance(content, str):
                        return content
            
            # If we couldn't find a direct markdown field, look for nested structure
            if 'document' in response_data:
                doc = response_data['document']
                if isinstance(doc, dict) and 'content' in doc:
                    return self.extract_markdown_from_response(doc['content'])
            
            # Last resort - recursive extraction
            return self.extract_text_recursively(response_data)
            
        return "# Extraction Failed\n\nCould not extract markdown content from the API response."
    
    def extract_text_recursively(self, data, depth=0, max_depth=5):
        """
        Recursively extract all text content from a complex JSON structure.
        """
        if depth > max_depth:
            return ""
            
        if isinstance(data, str):
            return data + "\n\n"
            
        if isinstance(data, list):
            result = ""
            for item in data:
                result += self.extract_text_recursively(item, depth + 1)
            return result
            
        if isinstance(data, dict):
            result = ""
            # Prioritize text-related keys
            for key in ['text', 'content', 'markdown', 'body', 'value']:
                if key in data:
                    result += self.extract_text_recursively(data[key], depth + 1)
            
            # If we didn't find priority keys, process all keys
            if not result:
                for key, value in data.items():
                    if not key.startswith('_'):  # Skip metadata-like fields
                        result += self.extract_text_recursively(value, depth + 1)
                        
            return result
            
        return ""
    
    def convert_pdf_to_markdown(self, pdf_path, output_path=None):
        """
        Main method to convert a PDF to Markdown.
        """
        # Extract content from the PDF
        response = self.extract_pdf_content(pdf_path)
        
        if not response:
            print("Failed to extract content from PDF. Exiting.")
            return False
        
        # Extract markdown content from the response
        markdown_content = self.extract_markdown_from_response(response)
        print(f"Conversion complete!")
        if output_path:
            # Save the raw response for debugging
            debug_path = f"{output_path}.debug.json"
            with open(debug_path, 'w', encoding='utf-8') as debug_file:
                json.dump(response, debug_file, indent=2)
            
            print(f"Raw API response saved to: {debug_path}")
            
            # Save the markdown content
            with open(output_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)
            print(f"Markdown saved to: {output_path}")
            return
         
        return markdown_content



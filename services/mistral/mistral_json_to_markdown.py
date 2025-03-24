#!/usr/bin/env python3

class MistralPDFToMarkdownConverter:
    def extract_markdown_from_json(self, json):
        """
        Extract markdown content from a JSON file and write it to a markdown file.
        
        Args:
            json_file (str): Path to the JSON file
            output_file (str): Path to the output markdown file
        """
        try:
            # Extract markdown content from each page
            markdown_content = ""
            if 'pages' in json:
                for page in json['pages']:
                    if 'markdown' in page:
                        markdown_content += page['markdown'] + "\n\n"
            
            return markdown_content
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return False


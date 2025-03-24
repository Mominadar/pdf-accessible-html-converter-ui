from services.mistral.mistral_pdf_to_json_urlonly import MistrlPdfToJsonUrlOnly
from services.mistral.mistral_json_to_markdown import MistralPDFToMarkdownConverter
from services.convert_markdown_html import MarkdownToHTMLConverter

class MistralService:
    def __init__(self):
        self.pdf_to_json_converter = MistrlPdfToJsonUrlOnly()
        self.json_to_md_converter = MistralPDFToMarkdownConverter()
        self.markdown_to_html_converter = MarkdownToHTMLConverter()
    
    def convert_pdf_to_html(self, pdf_path):
        json = self.pdf_to_json_converter.convert_pdf_to_json(pdf_path)
        markdown = self.json_to_md_converter.extract_markdown_from_json(json) 

        # with open("2.md") as f:
        #     markdown = f.read()
        html = self.markdown_to_html_converter.process_markdown_file(markdown)
        print("html", html)
        return html
        
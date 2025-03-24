from services.agentic.agentic_pdf_to_markdown import AgenticPDFToMarkdownConverter
from services.convert_markdown_html import MarkdownToHTMLConverter

class AgenticService:
    def __init__(self):
        self.pdf_to_markdown_converter = AgenticPDFToMarkdownConverter()
        self.markdown_to_html_converter = MarkdownToHTMLConverter()
    
    def convert_pdf_to_html(self, pdf_path):
        markdown = self.pdf_to_markdown_converter.convert_pdf_to_markdown(pdf_path)         
        html = self.markdown_to_html_converter.process_markdown_file(markdown)
        return html
        
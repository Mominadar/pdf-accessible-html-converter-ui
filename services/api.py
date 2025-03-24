from services.agentic.agentic_service import AgenticService
from services.mistral.mistral_service import MistralService

class ApiService():
    def __init__(self):
        self.agentic_service = AgenticService()
        self.mistral_service = MistralService()

    def convert_pdf_to_html(self, converter, pdf_path):
        if converter == "agentic":
            return self.agentic_service.convert_pdf_to_html(pdf_path)
        elif converter == "mistral":
            return self.mistral_service.convert_pdf_to_html(pdf_path)

        raise Exception("Invalid converter")
        
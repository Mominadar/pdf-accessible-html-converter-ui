# To Test the Agentic Document Extractor Try
python3 agentic-pdf-markdown.py pdfs/expressions2page.pdf output_tests/expressions2page.md
python3 agentic-markdown.py output_tests/expressions2page.md output_tests/expressions2page.html

# To Test the Mistral version
python3 mistral-pdf-json-urlonly.py <Edit URL in script> output_tests/output.json
python3 mistral-json-to-markdown.py output_tests/output.json output_tests/output.md
python3 mistral-markdown-html.py output_tests/output.md output_tests/output.html
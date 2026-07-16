import docx
from openpyxl import load_workbook
from pptx import Presentation
import os
import requests

class OfficeFileProcessor:
    def __init__(self, api_key):
        self.api_key = api_key

    def extract_text_from_word(self, file_path):
        doc = docx.Document(file_path)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text

    def extract_text_from_excel(self, file_path):
        wb = load_workbook(file_path)
        text = ''
        for sheet in wb.worksheets:
            for row in sheet.rows:
                for cell in row:
                    text += str(cell.value) + ' '
        return text

    def extract_text_from_pptx(self, file_path):
        presentation = Presentation(file_path)
        text = ''
        for slide in presentation.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + ' '
        return text

    def send_to_geminai(self, text):
        url = 'https://api.gemini.ai/v1/analyze'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.post(url, headers=headers, json={'text': text})
        return response.json()

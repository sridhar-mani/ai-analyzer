from typing import List, Generator, Union
import json
import csv
import chardet
from io import StringIO,BytesIO
import pandas as pd
import docx
import PyPDF2
import xml.etree.ElementTree as ET
import zipfile
import openpyxl
import email


class UniversalDocumentReader:
    
    def __init__(self, file_content: bytes, filename: str):
        self.content = file_content
        self.filename = filename.lower()
        self.text_content = None
    
    def detect_encoding(self) -> str:
        result = chardet.detect(self.content)
        return result['encoding'] or 'utf-8'
    
    def read_text_file(self) -> Generator[str, None, None]:
        encoding = self.detect_encoding()
        try:
            text = self.content.decode(encoding)
            for line in text.splitlines():
                yield line.strip()
        except UnicodeDecodeError as e:
            yield f"Error decoding file: {str(e)}"
    
    def read_json_file(self) -> Generator[str, None, None]:
        try:
            encoding = self.detect_encoding()
            text = self.content.decode(encoding)
            data = json.loads(text)
            
            def process_json(obj, parent_key=''):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        new_key = f"{parent_key}.{key}" if parent_key else key
                        if isinstance(value, (dict, list)):
                            yield from process_json(value, new_key)
                        else:
                            yield f"{new_key}: {value}"
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        new_key = f"{parent_key}[{i}]"
                        if isinstance(item, (dict, list)):
                            yield from process_json(item, new_key)
                        else:
                            yield f"{new_key}: {item}"
                else:
                    yield f"{parent_key}: {obj}"
            
            yield from process_json(data)
        except json.JSONDecodeError as e:
            yield f"Error parsing JSON: {str(e)}"
    
    def read_csv_file(self) -> Generator[str, None, None]:

        try:
            encoding = self.detect_encoding()
            text = self.content.decode(encoding)
            csv_reader = csv.reader(StringIO(text))
            for row in csv_reader:
                yield ', '.join(row)
        except Exception as e:
            yield f"Error reading CSV: {str(e)}"
    
    def read_excel_file(self) -> Generator[str, None, None]:

        try:
            wb = openpyxl.load_workbook(filename=BytesIO(self.content), data_only=True)
            for sheet in wb.sheetnames:
                ws = wb[sheet]
                yield f"Sheet: {sheet}"
                for row in ws.iter_rows(values_only=True):
                    yield ', '.join(str(cell) for cell in row if cell is not None)
        except Exception as e:
            yield f"Error reading Excel file: {str(e)}"
    
    def read_pdf_file(self) -> Generator[str, None, None]:

        try:
            from io import BytesIO
            pdf_reader = PyPDF2.PdfReader(BytesIO(self.content))
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                for line in text.splitlines():
                    if line.strip():
                        yield line.strip()
        except Exception as e:
            yield f"Error reading PDF: {str(e)}"
    
    def read_docx_file(self) -> Generator[str, None, None]:

        try:
            doc = docx.Document(BytesIO(self.content))
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    yield paragraph.text.strip()
        except Exception as e:
            yield f"Error reading DOCX: {str(e)}"
    
    def read_xml_file(self) -> Generator[str, None, None]:
        try:
            root = ET.fromstring(self.content)
            def process_element(element, level=0):
                indent = "  " * level
                if element.text and element.text.strip():
                    yield f"{indent}{element.tag}: {element.text.strip()}"
                for child in element:
                    yield from process_element(child, level + 1)
            yield from process_element(root)
        except ET.ParseError as e:
            yield f"Error parsing XML: {str(e)}"
    
    def read_email_file(self) -> Generator[str, None, None]:

        try:
            msg = email.message_from_bytes(self.content)
            yield f"Subject: {msg['subject']}"
            yield f"From: {msg['from']}"
            yield f"To: {msg['to']}"
            yield f"Date: {msg['date']}"
            
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        text = part.get_payload(decode=True).decode()
                        for line in text.splitlines():
                            if line.strip():
                                yield line.strip()
            else:
                text = msg.get_payload(decode=True).decode()
                for line in text.splitlines():
                    if line.strip():
                        yield line.strip()
        except Exception as e:
            yield f"Error reading email: {str(e)}"
    
    def read_lines(self) -> Generator[str, None, None]:
        file_readers = {
            '.txt': self.read_text_file,
            '.json': self.read_json_file,
            '.csv': self.read_csv_file,
            '.xlsx': self.read_excel_file,
            '.xls': self.read_excel_file,
            '.pdf': self.read_pdf_file,
            '.docx': self.read_docx_file,
            '.xml': self.read_xml_file,
            '.eml': self.read_email_file
        }
        
        ext = '.' + self.filename.split('.')[-1] if '.' in self.filename else ''
        
        reader = file_readers.get(ext, self.read_text_file)
        try:
            yield from reader()
        except Exception as e:
            yield f"Error processing file: {str(e)}"

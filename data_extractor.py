import fitz  # PyMuPDF
from dataclasses import dataclass
from typing import List
import re

@dataclass
class ExtractedData:
    full_address: str
    recipient_name: str
    street_address: str
    city_and_state: str
    zip_code: str
    estimated_value: float
    value_range_low: float
    value_range_high: float

class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
    
    def extract_data(self) -> List[ExtractedData]:
        extracted_data_list = []
        for page in self.doc: 
            text = page.get_text()
            if not text.strip():
                print("No text extracted from page in file: %s", self.pdf_path)
                continue

        
            # Extract address components using regex
            full_address_match = re.search(r"All Rights Reserved\.\s*\n\s*(.+)", text)
            name_match = re.search(r"Owner Name:\s*([^\n]+)", text)
            address_match = re.search(r"Mailing Address:\s*([^\n]+)", text)
            city_state_match = re.search(r"Tax Billing City & State:\s*([^\n]+)", text)
            zip_match = re.search(r"Tax Billing Zip:\s*(\d{5})", text)
            
            # Extract estimated values
            value_match = re.search(r"RealAVM[^:]*:\s*\$([0-9,]+)", text)
            range_high = re.search(r"High:\s*\$([0-9,]+)", text)
            range_low = re.search(r"Low:\s*\$([0-9,]+)", text)
        
            extracted_data_list.append(ExtractedData(
                full_address = full_address_match.group(1).strip() if full_address_match else "",
                recipient_name=name_match.group(1) if name_match else "",
                street_address=address_match.group(1) if address_match else "",
                city_and_state=city_state_match.group(1) if city_state_match else "",
                zip_code=zip_match.group(1) if zip_match else "",
                estimated_value=self._parse_currency(value_match.group(1)) if value_match else 0,
                value_range_low=self._parse_currency(range_low.group(1)) if range_low else 0,
                value_range_high=self._parse_currency(range_high.group(1)) if range_high else 0
            ))
        return extracted_data_list
    
    def _parse_currency(self, value: str) -> float:
        return float(value.replace(",", ""))
        
    def __del__(self):
        self.doc.close()
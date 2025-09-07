import os
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import grey
from data_extractor import ExtractedData
from PyPDF2 import PdfMerger
from docx import Document
import subprocess
import tempfile
import shutil
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from PyPDF2 import PdfReader, PdfWriter
import io


current_dir = os.path.dirname(os.path.abspath(__file__))

class DocumentGenerator:
    def __init__(self, output_dir: str, input_file: str):
        self.output_dir = output_dir 
        self.input_file = input_file
        self._setup_fonts()

    def _setup_fonts(self):
        # Register fonts
        # pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial', os.path.join(current_dir, 'fonts', 'arial.ttf')))
        pdfmetrics.registerFont(TTFont('Arial-Black', os.path.join(current_dir, 'fonts', 'arialbd.ttf')))
        pdfmetrics.registerFont(TTFont('Aptos', os.path.join(current_dir, 'fonts', 'Aptos.ttf')))
        pdfmetrics.registerFont(TTFont('Montserrat-Black-Italic', os.path.join(current_dir, 'fonts', 'Montserrat-BlackItalic.ttf')))
        pdfmetrics.registerFont(TTFont('Montserrat-Medium', os.path.join(current_dir, 'fonts', 'Montserrat-Medium.ttf')))
        pdfmetrics.registerFont(TTFont('Montserrat-BoldItalic', os.path.join(current_dir, 'fonts', 'Montserrat-BoldItalic.ttf')))
    def delete_generated_pdfs(self, pdf_paths):
        """ Delete all generated PDFs after merging """
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)


    def generate_pdf(self, data_list: list[ExtractedData]):
        merger = PdfMerger()  # Initialize PDF merger
        generated_pdfs = []  # Store paths of generated PDFs

        existing_pdf_path = os.path.join(current_dir, "docs", 'Page 2 REVISED NEW.pdf')  # Existing PDF for alternate pages
        file_base_name = os.path.basename(self.input_file)
        final_pdf_path = os.path.join(self.output_dir, f"fmtd_{file_base_name}")
        for index, data in enumerate(data_list):
            generated_pdf_path = os.path.join(self.output_dir, f"pg_{index + 1}_{file_base_name}")
            generated_pdfs.append(generated_pdf_path)

            # Create a new PDF page
            self.create_pdf_page(generated_pdf_path, data)

            # Append generated PDF page and existing PDF as alternating pages
            merger.append(generated_pdf_path)
            merger.append(existing_pdf_path)

        # Save the final merged PDF
        merger.write(final_pdf_path)
        merger.close()

        # Cleanup generated PDFs
        self.delete_generated_pdfs(generated_pdfs)

    def create_pdf_page(self, pdf_path, data: ExtractedData):
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Convert inches to points (1 inch = 72 points)
        left_margin = 1 * 72  # 1 inch from left
        right_margin = 8.5 * 72 - 1 * 72  # 1 inch from right
        top_margin = 11 * 72 - 0.5 * 72  # 0.5 inch from top
        line_height = 13
        center_x = (left_margin + right_margin) / 2

        # Template text with placeholders
        template_text = f"""Mike Wilen Real Estate
        270 Hennepin Ave #1111
        Minneapolis, MN 55401

        


        
        
        {data.recipient_name}
        {data.street_address}
        {data.city_and_state} {data.zip_code}






        """

        # Add text to PDF
        c.setFont("Aptos", 13)
        y_position = top_margin
        for line in template_text.splitlines():
            c.drawString(left_margin, y_position, line.strip())
            y_position -= line_height
        
        c.setFont("Montserrat-Black-Italic", 20)
        c.drawCentredString(center_x, y_position, "WHAT YOUR HOME COULD BE WORTH TODAY")
        y_position -= 1 * line_height  # Add more space


        # Center-align remaining text
        remaining_text = """Pricing your home correctly is one of the most important steps in successfully
marketing your property. A home can carry different values, one for the tax assessor,
another for an appraiser, and yet another for you as the owner. Prospective buyers
may also view its worth differently depending on their individual needs. The
estimate provided comes from an Automated Valuation Model (AVM). An AVM is a
computer-based system that evaluates recent sales, and market trends to generate
a value. Depending on the quality and depth of available data, this estimate may
closely reflect your home's true market value, or it may vary significantly.
        """
        
        c.setFont("Montserrat-Medium", 13)
        for line in remaining_text.splitlines():
            if line.strip():  # Skip empty lines
                c.drawCentredString(center_x, y_position, line.strip())
            y_position -= line_height
        y_position -=  1.5*line_height
        
        # Center-align full address and estimated price
        c.setFont("Montserrat-Medium", 18)
        c.drawCentredString(center_x, y_position, data.full_address)
        y_position -= 2* line_height

        middle_title_text = "Estimated List Price:"
        c.drawCentredString(center_x, y_position, middle_title_text)
        y_position -= 2*line_height

        c.setFont("Montserrat-Black-Italic", 18)
        c.drawCentredString(center_x, y_position, f"${data.value_range_high:,.2f}")
        y_position -= 2 * line_height  # Add more space
        
        y_position -= 10*line_height
        additional_text = """
        LIST WITH US
        YOUR PROPERTY, OUR PRIORITY
        TALK / TEXT 612-400-9000
        
        
        
        """
        c.setFont("Montserrat-Black-Italic", 20)
        for line in additional_text.splitlines():
            if line.strip():
                c.drawCentredString(center_x, y_position, line.strip())
            y_position -= 1.5 * line_height
        

        # Add logo at the center of the footer using the image's actual size
        logo_path = os.path.join(current_dir, 'images', 'Picture1.png')
        logo = ImageReader(logo_path)
        logo_width, logo_height = logo.getSize()
        scaled_width = logo_width * 0.35
        scaled_height = logo_height * 0.35
        logo_x = center_x - (scaled_width / 2)
        # Place the logo just above the footer text
        logo_y = 0.3 * 72 + 18  # 16 points above the footer text
        c.drawImage(logo, logo_x, logo_y, width=scaled_width, height=scaled_height, mask='auto')
        # the footer text
        footer_y = 0.3 * 72  # Footer position 0.3 inch from bottom
        c.setFont("Montserrat-BoldItalic", 10.5)
        c.drawCentredString(center_x, footer_y, f"MIKEWILEN.COM   1MW.COM   NONNMLS.COM   MINNESOTATEAM.COM   LAKEMINNETONKATEAM.COM")

        c.save() # Save the first page

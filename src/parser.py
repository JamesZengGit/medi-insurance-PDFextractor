import pdfplumber

def extract_pdf_lines(pdf_loc: str):
    lines = []
    with pdfplumber.open(pdf_loc) as pdf:
        for page in pdf.pages:
            text_piece = page.extract_text()
            if text_piece:
                lines.extend(text_piece.split("\n"))
    return lines

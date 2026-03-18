import pdfplumber

def extract_text_from_pdf(file):
    '''
    Extracts plain text from an uploaded PDF file
    Args: 
        file: FileStorage object from Flask Request
    Returns:
        str: Extracted text from the PDF
    '''

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text.strip()
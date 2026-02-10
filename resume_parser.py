import PyPDF2
import io

def extract_text_from_pdf(uploaded_file):
    """
    Takes an uploaded PDF file and extracts all the text from it.
    
    Why we need this:
    - Resumes are usually PDFs
    - We can't do NLP on a PDF directly - we need raw text first
    - PyPDF2 reads each page and pulls out the text
    """
    text = ""
    
    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    
    # Loop through every page and collect the text
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    return text.strip()


def clean_text(text):
    """
    Cleans up the extracted text so our NLP model works better.
    
    Why we need this:
    - PDFs often have weird characters, extra spaces, or formatting artifacts
    - Cleaner text = better similarity scores
    """
    import re
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep letters, numbers, and basic punctuation
    text = re.sub(r'[^\w\s\.,\-\(\)@]', ' ', text)
    
    # Convert to lowercase for consistency
    text = text.lower().strip()
    
    return text
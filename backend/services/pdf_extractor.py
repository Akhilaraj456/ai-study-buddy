from typing import Dict, List
from PyPDF2 import PdfReader


def extract_text_from_pdf(file) -> Dict:
    """
    Extracts text from a PDF file.

    Returns:
        {
            "text": str,
            "num_pages": int,
            "warnings": List[str]
        }
    """
    warnings: List[str] = []
    text_chunks: List[str] = []

    try:
        reader = PdfReader(file)
        num_pages = len(reader.pages)

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

        full_text = "\n".join(text_chunks)

        if not full_text.strip():
            warnings.append("No extractable text found (possibly a scanned PDF)")

        return {
            "text": full_text,
            "num_pages": num_pages,
            "warnings": warnings
        }

    except Exception as e:
        raise RuntimeError(f"Failed to extract PDF text: {str(e)}")

def validate_pdf(filename: str) -> None:
    """
    Validates that the uploaded file looks like a PDF.
    Raises ValueError if invalid.
    """
    if not filename.lower().endswith(".pdf"):
        raise ValueError("Uploaded file is not a PDF")
    
    

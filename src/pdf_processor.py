import fitz


def extract_text_from_pdf(pdf_bytes):
    """
    Extract text from each page of a PDF.

    Returns:
        List of dictionaries containing page number and text.
    """

    document = fitz.open(stream=pdf_bytes, filetype="pdf")

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        if text.strip():
            pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

    document.close()

    return pages
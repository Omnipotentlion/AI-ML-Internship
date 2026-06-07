import fitz

def extract_pdf_text(pdf_path):

    text = ""

    try:

        doc = fitz.open(pdf_path)

        for page in doc:

            text += page.get_text()

        doc.close()

        return text

    except Exception as e:

        print(e)

        return ""
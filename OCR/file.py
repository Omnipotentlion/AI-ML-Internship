#C:\Users\YASH\AppData\Local\Programs\Tesseract-OCR

import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\YASH\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

import pytesseract

print(pytesseract.get_tesseract_version())
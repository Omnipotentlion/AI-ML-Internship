import cv2
import pytesseract
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\YASH\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def preprocess_image(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError("Image not found. Check the file path.")

    
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    
    gray = cv2.medianBlur(gray, 3)

    
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return image, gray, thresh


def extract_text(image_path):
    image, gray, thresh = preprocess_image(image_path)

    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh, config=config)

    print("Extracted Text:\n")
    print(text)

    plt.figure(figsize=(15, 6))

    plt.subplot(1, 3, 1)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title("Grayscale")
    plt.imshow(gray, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.title("Thresholded")
    plt.imshow(thresh, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("\nText saved to extracted_text.txt")


if __name__ == "__main__":
    extract_text("testocr.jpg")
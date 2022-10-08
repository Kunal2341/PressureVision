from PIL import Image
from pyzbar.pyzbar import decode
import os


def pyzbarDecode(imgPath):
    result = decode(Image.open(imgPath))
    for barcode in result:
        return(barcode.data.decode("utf-8"))

print(os.getcwd())
print(type(pyzbarDecode("Frame2.jpg")))
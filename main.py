from pyzbar import pyzbar
import cv2
from urltitle import URLTitleReader

def read_barcode (frame):
    barcodes = pyzbar.decode(frame)
    barcode_info = []

    for obj in barcodes:
        barcode_info.append(obj.data.decode("utf-8"))

    if len(barcode_info) > 0:
        return barcode_info
    else:
        return "Please scan again"

def lookup_barcode (barcode):
    url = "https://icheck.vn/san-pham/" + barcode

    try:
        reader = URLTitleReader()
        return reader.title(url)
    except:
        return "Not found the product"

def main():
    # get the image
    image_path = "./images/4.jpg"
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # # read the barcode
    numbers = read_barcode(image)
    print(numbers)

    # lookup the barcode
    for number in numbers:
        title = lookup_barcode(number)
        print(title)


if __name__ == "__main__":
    main()
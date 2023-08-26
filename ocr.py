from pyzbar import pyzbar
import cv2
import requests
from lxml import html
import re

def read_barcode (frame):
    barcodes = pyzbar.decode(frame)
    barcode_info = None

    for obj in barcodes:
        barcode_info = (obj.data.decode("utf-8"))

    if len(barcode_info) > 0:
        return barcode_info
    else:
        return "Please scan again"

def lookup_barcode (barcode):
    url = "https://icheck.vn/san-pham/" + barcode

    try:
        response = requests.get(url)
        tree = html.fromstring(response.content)
        title = tree.xpath('//title/text()')[0]
        description = tree.xpath('//meta[@name="description"]/@content')[0]

        price_pattern = r"Giá: (.*?) đ"
        price = re.search(price_pattern, description).group(1).replace(",", "")

        publisher_pattern = r"của (.*?) iCheck.vn"
        publisher = re.search(publisher_pattern, description).group(1)

        return title, price, publisher
    except:
        return "Not found the product"

def return_product(path):
    # get the image
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # # read the barcode
    number = read_barcode(image)

    # lookup the barcode
    title = lookup_barcode(number)[0]
    price = lookup_barcode(number)[1]
    publisher = lookup_barcode(number)[2]

    result = {
        "barcode": int(number),
        "title": title,
        "price": int(price),
        "publisher": publisher
    }

    return result

# print(return_product('./test_imgs/2.jpg'))
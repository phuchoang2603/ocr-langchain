from flask import Flask, request, jsonify
from ocr import return_product
from os import mkdir
import os.path as path

if(not(path.exists('./output_imgs'))):
    mkdir('./output_imgs')

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    img = request.files['img']
    img_path = './output_imgs/img.jpg'
    img.save(img_path)
    product = return_product(img_path)

    return jsonify(product)
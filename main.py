from flask import Flask, request, jsonify
import os
from os import mkdir
import os.path as path
# our modules
from ocr import return_product
from google import search_product_links

if(not(path.exists('./output'))):
    mkdir('./output')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def ocr():
    img_url = request.args.get('url')
    product = return_product(img_url)
    query = "Hướng dẫn phân biệt hàng thật hàng giả " + product['title']

    # search product
    search_result = search_product_links(query)

    return jsonify({
        "status": "success",
        "product": product,
        "search_result": search_result
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
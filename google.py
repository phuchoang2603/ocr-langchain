import requests
import urllib.parse
import json
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API = os.getenv("GOOGLE_API")
GOOGLE_SEARCH_ID = os.getenv("GOOGLE_SEARCH_ID")

def search_product (title):
    q = "phân biệt hàng giả hàng thật " + title

    data = {
    "key": GOOGLE_API,
    "cx": GOOGLE_SEARCH_ID,
    "q": q
    }

    # Convert data to a query string and encode it
    query_string = urllib.parse.urlencode(data)
    url = "https://www.googleapis.com/customsearch/v1?" + query_string

    # Make the HTTP request
    response = requests.get(url)
    data = response.json()["items"]

    for result in data:
        process_individual_result(result)

def process_individual_result (result):
    link = result["link"]

    print(link)

search_product("iphone 7")
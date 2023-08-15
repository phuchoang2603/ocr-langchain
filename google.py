import requests
import urllib.parse
import json

key = "AIzaSyBpjFbbzp02ust_JMBDy-45T9jczDLbsDk"
cx = "2009e1f0d098640da"

def search_product (title):
    q = "phân biệt hàng giả hàng thật " + title

    data = {
    "key": key,
    "cx": cx,
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
    title = result["title"]
    link = result["link"]
    thumbnail = result["pagemap"]["cse_thumbnail"][0]["src"]

    print(title)
    print(link)
    print(thumbnail)
    print("--------------------------------------------------")
    

search_product("iphone 7")
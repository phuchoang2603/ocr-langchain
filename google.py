import requests
import urllib.parse
from bs4 import BeautifulSoup
import json
from langchain.chat_models import ChatOpenAI
from playwright.async_api import async_playwright
from langchain.chains import create_extraction_chain
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

GOOGLE_API = os.getenv("GOOGLE_API")
GOOGLE_SEARCH_ID = os.getenv("GOOGLE_SEARCH_ID")

def search_product_links (query):
    """Tìm kiếm các link giúp hỗ trợ phân biệt hàng thật hàng giả của một sản phẩm"""
    
    data = {
    "key": GOOGLE_API,
    "cx": GOOGLE_SEARCH_ID,
    "q": query
    }

    # Convert data to a query string and encode it
    query_string = urllib.parse.urlencode(data)
    url = "https://www.googleapis.com/customsearch/v1?" + query_string

    # Make the HTTP request and get five url to provide the model
    response = requests.get(url)
    data = response.json()["items"][:5]

    # Return list of urls in json format
    output = []
    for item in data:
        title = item["title"]
        link = item["link"]
        provider = item["displayLink"]
        output.append({
            "title": title,
            "link": link,
            "provider": provider
        })

    print ("Done searching")

    # write to json file
    with open('search-result.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    return output

async def run_playwright(site):
    """Trích xuất thông tin từ link hướng dẫn phân biệt hàng thật hàng giả của một sản phẩm"""

    data = ""
    print ("Getting information from " + site)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        page = await browser.new_page()
        await page.goto(site)
        
        page_source = await page.content()
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Find the "article" tag
        article_tag = soup.find("article")
        
        if article_tag:
            # Extract text content from "article" tag
            text = article_tag.get_text()
        else:
            # Find an element with "article" in its class
            element_with_article_class = soup.find(class_=lambda value: value and "article" in value)
        
            if element_with_article_class:
                # Extract text content from element with "article" class
                text = element_with_article_class.get_text()
            else:
                text = ""
        
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        data = '\n'.join(chunk for chunk in chunks if chunk)

        await browser.close()
    
    return data

async def process_individual_link(item):

    content = await run_playwright(item["link"])

    output = f"""Title: {item["title"]}
Link: {item["link"]}
Provider: {item["provider"]}
Content: {content}
------------------------------------------
"""

    # Write output to txt file
    with open('output.txt', 'a', encoding='utf-8') as f:
        f.write(output)

async def run_async_processing(query):
    # Use asyncio.gather() to concurrently execute all the instances of process_item()
    tasks = [process_individual_link(item) for item in search_product_links(query)]
    await asyncio.gather(*tasks)

# clear output.txt
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("")

asyncio.run(run_async_processing("làm thế nào để phân biệt hàng thật hàng giả của iphone 7"))

# get data from output.txt
with open('output.txt', 'r', encoding='utf-8') as f:
    inp = f.read()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
stuctured_schema = {
    "properties": {
        "title": {"type": "string"},
        "link": {"type": "string"},
        "provider": {"type": "string"},
        "steps-to-identify": {"type": "string"}
    }
}
extraction_chain = create_extraction_chain(stuctured_schema, llm)
extraction_chain.run(inp)
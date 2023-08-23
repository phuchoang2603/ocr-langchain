import requests
import urllib.parse
from bs4 import BeautifulSoup
import json
from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.agents import tool
from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API = os.getenv("GOOGLE_API")
GOOGLE_SEARCH_ID = os.getenv("GOOGLE_SEARCH_ID")

@tool
def search_product_links (query: str) -> str:
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
        output.append({
            "title": title,
            "link": link
        })

    return json.dumps(output)


@tool
def extract_info_from_tutorial(urls_array: str) -> str:
    """Trích xuất thông tin từ các link hướng dẫn phân biệt hàng thật hàng giả của một sản phẩm
    
    Đầu vào của tool này là một mảng các link hướng dẫn đó"""

    # Load HTML from urls
    loader = AsyncHtmlLoader(urls_array)
    htmls = loader.load()

    # Transform HTML to BeautifulSoup
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(htmls, tags_to_extract=["article"])

    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, 
                                                                    chunk_overlap=0)
    splits = splitter.split_documents(docs_transformed)


llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
tools = [search_product_links, extract_info_from_tutorial]
agent = initialize_agent(tools, llm, agent='chat-zero-shot-react-description', verbose=True)

result = agent.run("làm thế nào để phân biệt hàng thật hàng giả của iphone 7, trả lời theo ngôn ngữ tiếng việt")
print(result)
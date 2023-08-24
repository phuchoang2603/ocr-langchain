import requests
import urllib.parse
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain

# Schema
schema = {
    "properties": {
        "fake product": {"type": "string"},
        "fake product image url": {"type": "string"},
        "real product": {"type": "string"},
        "real product image url": {"type": "string"}
    },
    "required": ["fake product", "real product"]
}

load_dotenv()
llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
tools = load_tools(["serpapi"], llm=llm)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
chain = create_extraction_chain(schema, llm)
agent.run("cách để phân biệt hàng giả hàng thật của iphone 7")
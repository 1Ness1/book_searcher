import requests
from bs4 import BeautifulSoup
import json



def parse_flibusta(query):
    query.strip()
    if not query: 
        return None

    url = "https://flibusta.is/booksearch"
    params = {"ask": query}

    response = requests.get(url, params=params)
    response.encoding = "utf=8"

    soup = BeautifulSoup(response.text, "html.parser")

    search_results = []

    for link in soup.select("#main ul li a"):
        title = link.text.strip()
        href = link.get("href")
        domain = "https://flibusta.is"
        item = {"title": title, "url": f"{domain}{href if href else None}"}

        if href:
            if "/b/" in href:
                item["type"] = "book"
            elif "/a/" in href:
                item["type"] = "author"
            else:
                item["type"] = "unkown"

        search_results.append(item)
    
    return search_results

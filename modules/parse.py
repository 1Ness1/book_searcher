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

    item_container = {
            "books": [],
            "authors": [],
            "sequence": [],
            "unknown": [],
    }

    for link in soup.select("#main ul li a"):
        title = link.text.strip()
        href = link.get("href")
        domain = "https://flibusta.is"

        item = {
            "title": title,
            "url": f"{domain}{href if href else None}"
        }

        if href:
            if "/b/" in href:
                item_container["books"].append(item)
            elif "/a/" in href:
                item_container["authors"].append(item)
            elif "/sequence/" in href:
                item_container["sequence"].append(item)
            else:
                item_container["unknown"].append(item)

    return item_container

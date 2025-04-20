import requests
from bs4 import BeautifulSoup
import json

results = []

with open("books.txt", "r", encoding="utf-8") as f:
    for query in f:
        query = query.strip()
        if not query: 
            continue

        url = "https://flibusta.is/booksearch"
        params = {"ask": query}

        response = requests.get(url, params=params)
        response.encoding = "utf=8"

        soup = BeautifulSoup(response.text, "html.parser")

        print(f"\nРезультаты поиска по запросу: {query}\n")

        search_results = {"query": query, "items": []}

        for link in soup.select("#main ul li a"):
            title = link.text.strip()
            href = link.get("href")
            domain = "https://flibusta.is"
            item = {"title": title, "url": f"{domain}{href if href else None}"}

            if href:
                if "/b/" in href:
                    item["type"] = "Book"
                elif "/a/" in href:
                    item["type"] = "Author"
                else:
                    item["type"] = "Unkown"

            search_results["items"].append(item)
        
        results.append(search_results)
            
        
print(json.dumps(results, ensure_ascii=False, indent=4))

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
import logging
from enum import Enum
from typing import List, Optional, Dict
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl

# Logger
logger = logging.getLogger("flibusta_parser")
logging.basicConfig(level=logging.INFO)

# Types
class ItemType(str, Enum):
    BOOK = "books"
    AUTHOR = "authors"
    SEQUENCE = "sequence"
    UNKNOWN = "unknown"

class SearchItem(BaseModel):
    title: str
    url: HttpUrl

class SearchResult(BaseModel):
    books: List[SearchItem] = []
    authors: List[SearchItem] = []
    sequence: List[SearchItem] = []
    unknown: List[SearchItem] = []

# Constants
BASE_URL = "https://flibusta.is"
SEARCH_URL = f"{BASE_URL}/booksearch"

# Functions
def normalize_query(query: str) -> Optional[str]:
    clean = query.strip()
    return clean if clean else None

def classify_href(href: str) -> ItemType:
    if "/b/" in href:
        return ItemType.BOOK
    elif "/a/" in href:
        return ItemType.AUTHOR
    elif "/sequence/" in href:
        return ItemType.SEQUENCE
    return ItemType.UNKNOWN

def extract_items(soup: BeautifulSoup) -> SearchResult:
    result: Dict[ItemType, List[SearchItem]] = {
        t: [] for t in ItemType
    }

    for link in soup.select("#main ul li a"):
        title = link.text.strip()
        href = link.get("href")

        if not href:
            continue

        try:
            item_type = classify_href(href)
            item = SearchItem(title=title, url=f"{BASE_URL}{href}")
            result[item_type].append(item)
        except Exception as e:
            logger.warning(f"Validation error of element '{title}': {e}")

    return SearchResult(
        books=result[ItemType.BOOK],
        authors=result[ItemType.AUTHOR],
        sequence=result[ItemType.SEQUENCE],
        unknown=result[ItemType.UNKNOWN],
    )

def parse_flibusta(query: str) -> Optional[SearchResult]:
    normalized = normalize_query(query)
    if not normalized:
        logger.warning("Empty request")
        return None
    
    try:
        response = requests.get(SEARCH_URL, params={"ask": normalized}, timeout=10)
        response.encoding = "utf-8"

        if response.status_code != 200:
            logger.error(f"Http Error: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        return extract_items(soup)

    except requests.RequestException as e:
        logger.error(f"Error with connection to Flibusta: '{e}'")
        return None
    
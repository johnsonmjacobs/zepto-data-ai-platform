"""Scrape book data from books.toscrape.com (a site built for scraping practice)."""

import truststore
truststore.inject_into_ssl()  # use the Windows cert store so the office proxy cert is trusted

import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "zepto-capstone-student-scraper/1.0"}

# 4 categories -> about 85 books, comfortably above the 60 required
TARGET_CATEGORIES = ["Travel", "Mystery", "Historical Fiction", "Science Fiction"]


def get_soup(url):
    """Fetch a page and check the HTTP status explicitly."""
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    resp.encoding = "utf-8"  # otherwise the pound sign comes out garbled
    return BeautifulSoup(resp.text, "html.parser")


def get_category_urls():
    """Read the sidebar on the home page and map category name -> URL."""
    soup = get_soup(BASE_URL)
    links = soup.select("div.side_categories ul li ul li a")
    return {a.get_text(strip=True): urljoin(BASE_URL, a["href"]) for a in links}


def parse_book(article, category):
    """Pull the raw fields out of one book card. Missing pieces become None
    so the cleaning step can deal with them instead of crashing here."""
    def safe(fn):
        try:
            return fn()
        except (AttributeError, KeyError, IndexError, TypeError):
            return None

    return {
        "title": safe(lambda: article.h3.a["title"]),
        "price": safe(lambda: article.select_one("p.price_color").get_text(strip=True)),
        "star_rating": safe(lambda: article.select_one("p.star-rating")["class"][1]),
        "availability": safe(lambda: article.select_one("p.availability").get_text(strip=True)),
        "category": category,
    }


def scrape_category(name, url, delay=0.5):
    """Walk through every paginated page of one category."""
    books = []
    while url:
        soup = get_soup(url)
        for article in soup.select("article.product_pod"):
            books.append(parse_book(article, name))
        nxt = soup.select_one("li.next a")
        url = urljoin(url, nxt["href"]) if nxt else None
        time.sleep(delay)  # be polite to the server
    return books


def scrape_all():
    category_urls = get_category_urls()
    rows = []
    for name in TARGET_CATEGORIES:
        if name not in category_urls:
            print(f"[warn] category '{name}' not found, skipping")
            continue
        got = scrape_category(name, category_urls[name])
        print(f"[scrape] {name}: {len(got)} books")
        rows.extend(got)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = scrape_all()
    print(df.head())
    print("Total rows:", len(df))
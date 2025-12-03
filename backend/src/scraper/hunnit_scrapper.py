import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random

BASE = "https://hunnit.com"

def fetch_listing(page_url=None, max_products=30):
    url = page_url or f"{BASE}/collections/all"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # example selectors — adjust after inspecting site
    cards = soup.select("a.product-card") or soup.select(".product-grid-item a")
    results = []
    for a in cards[:max_products]:
        link = a.get("href")
        full = urljoin(BASE, link)
        title = a.get_text(strip=True)
        # fallback: try to find an img and price inside element
        price = None
        image = None
        img = a.select_one("img")
        if img:
            image = img.get("src") or img.get("data-src")
            if image and image.startswith("//"):
                image = "https:" + image
        # if title blank, pull from nested element
        if not title:
            t = a.select_one(".product-title") or a.select_one(".card-title")
            title = t.get_text(strip=True) if t else "Untitled"

        results.append({"title": title, "source_url": full, "image_url": image, "price": price})
    return results

def fetch_product_detail(product_url):
    resp = requests.get(product_url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    title_el = soup.select_one("h1.product-title") or soup.select_one("h1")
    title = title_el.get_text(strip=True) if title_el else None

    price_el = soup.select_one(".product-price") or soup.select_one(".price")
    price = price_el.get_text(strip=True) if price_el else None

    # description and features
    desc_el = soup.select_one(".product-description") or soup.select_one("#description") or soup.select_one(".description")
    description = desc_el.get_text(strip=True) if desc_el else None

    features = []
    for li in soup.select(".product-features li"):
        features.append(li.get_text(strip=True))

    # fallback: find bullets in description
    if not features:
        for ul in soup.select(".description ul"):
            for li in ul.select("li"):
                features.append(li.get_text(strip=True))

    image_el = soup.select_one(".product-image img") or soup.select_one("img")
    image_url = None
    if image_el:
        image_url = image_el.get("src") or image_el.get("data-src")
        if image_url and image_url.startswith("//"):
            image_url = "https:" + image_url

    category_el = soup.select_one(".breadcrumb li:last-child") or soup.select_one(".product-category")
    category = category_el.get_text(strip=True) if category_el else None

    return {
        "title": title,
        "price": price,
        "description": description,
        "features": features,
        "image_url": image_url,
        "category": category,
        "source_url": product_url
    }

# polite scraping: random sleep
def polite_sleep(a=0.8, b=1.8):
    time.sleep(random.uniform(a, b))

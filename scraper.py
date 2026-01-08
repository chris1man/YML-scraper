import requests
from bs4 import BeautifulSoup
from settings import (
    BASE_URL,
    CATALOG_URL,
    HEADERS,
    FORCE_PRICE_ONE,
    DEFAULT_CATEGORY_ID
)


def get_product_links():
    response = requests.get(CATALOG_URL, headers=HEADERS)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "lxml")
    links = []

    for item in soup.select(".ty-grid-list__item a[href]"):
        href = item.get("href")

        if href.startswith("/"):
            href = BASE_URL + href

        if href.startswith(BASE_URL):
            links.append(href)

    return list(set(links))


def detect_category_id(url):
    if "/cvety-ohapkoy/" in url:
        return 3
    if "/rozy/" in url:
        return 2
    if "/bukety/" in url:
        return 1
    return DEFAULT_CATEGORY_ID


def parse_product(url):
    response = requests.get(url, headers=HEADERS)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "lxml")

    name_tag = soup.select_one("h1.ty-product-block-title")
    name = name_tag.text.strip() if name_tag else "Без названия"

    if FORCE_PRICE_ONE:
        price = "1"
    else:
        price_tag = soup.select_one("span.ty-price-num")
        price = price_tag.text.strip() if price_tag else "1"

    image_tag = soup.select_one("img.ty-pict")
    image = image_tag["src"] if image_tag else ""

    description = f"{name}. Свежие цветы с доставкой по Томску."

    return {
        "name": name,
        "price": price,
        "url": url,
        "image": image,
        "category_id": detect_category_id(url),
        "description": description,
        "available": "true"
    }

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
    response = requests.get(CATALOG_URL, headers=HEADERS, timeout=20)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "lxml")

    links = set()

    for a in soup.select(".ty-grid-list__item-name a[href]"):
        href = a.get("href", "").strip()

        if not href:
            continue

        if href.startswith("/"):
            href = BASE_URL + href

        if href.startswith(BASE_URL) and len(href) > 40:
            links.add(href)

    return list(links)


def detect_category_id(url):
    if "/cvety-ohapkoy/" in url:
        return 3
    if "/rozy/" in url:
        return 2
    if "/bukety/" in url:
        return 1
    return DEFAULT_CATEGORY_ID


def parse_product(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")

    name_tag = soup.select_one("h1.ty-product-block-title")
    if not name_tag:
        print("⛔ Не товар:", url)
        return None

    name = name_tag.text.strip()
    if len(name) < 5:
        print("⛔ Плохое имя:", url)
        return None

    # Цена
    if FORCE_PRICE_ONE:
        price = "1"
    else:
        price_tag = soup.select_one("span.ty-price-num")
        price = price_tag.text.strip() if price_tag else "1"

    # Картинка
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

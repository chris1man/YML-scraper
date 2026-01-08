# scraper.py

import requests
from bs4 import BeautifulSoup
from settings import (
    BASE_URL,
    CATALOG_URL,
    HEADERS,
    DEFAULT_CATEGORY_ID,
    FORCE_PRICE_ONE
)


def get_product_links():
    response = requests.get(CATALOG_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "lxml")

    links = []

    for item in soup.select(".ty-grid-list__item"):
        a = item.select_one("a[href]")
        if not a:
            continue

        href = a.get("href")
        if href.startswith("/"):
            href = BASE_URL + href

        if href.startswith(BASE_URL):
            links.append(href)

    return list(set(links))


def detect_category_id_by_url(url):
    if "/cvety-ohapkoy/" in url:
        return 3
    if "/rozy/" in url:
        return 2
    if "/bukety/" in url:
        return 1

    return DEFAULT_CATEGORY_ID


def parse_product(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "lxml")

    # Название
    name_tag = soup.select_one("h1.ty-product-block-title")
    name = name_tag.text.strip() if name_tag else "Без названия"

    # Цена
    if FORCE_PRICE_ONE:
        price = "1"
    else:
        price_tag = soup.select_one("span.ty-price-num")
        price = (
            price_tag.text
            .replace("\xa0", "")
            .replace(" ", "")
            .replace("₽", "")
        ) if price_tag else "1"

    # Картинка
    image_tag = soup.select_one("img.ty-pict")
    image = image_tag["src"] if image_tag else ""

    # Категория
    category_id = detect_category_id_by_url(url)

    # Description
    description = f"{name}. Свежие цветы с доставкой по Томску."

    return {
        "name": name,
        "price": price,
        "url": url,
        "image": image,
        "category_id": category_id,
        "description": description,
        "available": "true"
    }

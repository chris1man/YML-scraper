import requests
from bs4 import BeautifulSoup
from settings import BASE_URL, HEADERS


def get_html():
    r = requests.get(BASE_URL, headers=HEADERS, timeout=20)
    r.encoding = "utf-8"
    return r.text


def parse_products():
    html = get_html()
    soup = BeautifulSoup(html, "lxml")

    categories = {}
    products = []

    category_id_counter = 1
    product_id_counter = 1

    containers = soup.select(".ty-mainbox-simple-container")

    for container in containers:
        h2 = container.select_one(".ty-mainbox-simple-title")
        body = container.select_one(".ty-mainbox-simple-body")

        if not h2 or not body:
            continue

        category_name = h2.get_text(strip=True)

        if not category_name:
            continue


        items = body.select(".ty-grid-list__item .product-title")

        if not items:
            continue

        if category_name not in categories:
            categories[category_name] = category_id_counter
            category_id_counter += 1

        category_id = categories[category_name]

        product_blocks = body.select(".ty-grid-list__item")

        for item in product_blocks:
            title_el = item.select_one(".product-title")
            link_el = item.select_one(".product-title[href]")
            img_el = item.select_one("img")

            if not title_el or not link_el:
                continue

            name = title_el.get_text(strip=True)
            url = link_el.get("href", "").strip()
            picture = img_el.get("src", "").strip() if img_el else ""

            if not name or not url:
                continue

            products.append({
                "id": product_id_counter,
                "name": name,
                "url": url,
                "picture": picture,
                "category_id": category_id,
                "description": f"{name}. Свежие цветы с доставкой по Томску."
            })

            product_id_counter += 1

    return products, categories

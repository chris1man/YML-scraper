# yml.py

from xml.etree.ElementTree import Element, SubElement, ElementTree
from datetime import datetime
from settings import SHOP_NAME, SHOP_URL, CURRENCY, CATEGORIES


def generate_yml(products):
    yml = Element(
        "yml_catalog",
        date=datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    shop = SubElement(yml, "shop")

    SubElement(shop, "name").text = SHOP_NAME
    SubElement(shop, "url").text = SHOP_URL

    # 🔥 ОБЯЗАТЕЛЬНО ДЛЯ ЯНДЕКС БИЗНЕС
    categories_el = SubElement(shop, "categories")
    for cid, cname in CATEGORIES.items():
        cat = SubElement(categories_el, "category", id=str(cid))
        cat.text = cname

    offers = SubElement(shop, "offers")

    for i, product in enumerate(products, start=1):
        offer = SubElement(
            offers,
            "offer",
            id=str(i),
            available=product["available"]
        )

        SubElement(offer, "name").text = product["name"]
        SubElement(offer, "price").text = product["price"]
        SubElement(offer, "currencyId").text = CURRENCY
        SubElement(offer, "categoryId").text = str(product["category_id"])
        SubElement(offer, "picture").text = product["image"]
        SubElement(offer, "url").text = product["url"]
        SubElement(offer, "description").text = product["description"]

    ElementTree(yml).write(
        "feed.yml",
        encoding="utf-8",
        xml_declaration=True
    )

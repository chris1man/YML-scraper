import xml.etree.ElementTree as ET
from xml.dom import minidom
from settings import SHOP_NAME, SHOP_URL, CURRENCY, FORCE_PRICE_ONE


def generate_xml(products, categories, output_file):
    root = ET.Element("yml_catalog")
    shop = ET.SubElement(root, "shop")

    ET.SubElement(shop, "name").text = SHOP_NAME
    ET.SubElement(shop, "url").text = SHOP_URL

    categories_el = ET.SubElement(shop, "categories")
    for name, cid in categories.items():
        cat = ET.SubElement(categories_el, "category", id=str(cid))
        cat.text = name

    offers_el = ET.SubElement(shop, "offers")

    for product in products:
        offer = ET.SubElement(
            offers_el,
            "offer",
            id=str(product["id"]),
            available="true"
        )

        ET.SubElement(offer, "name").text = product["name"]
        ET.SubElement(offer, "price").text = "1" if FORCE_PRICE_ONE else "0"
        ET.SubElement(offer, "currencyId").text = CURRENCY
        ET.SubElement(offer, "categoryId").text = str(product["category_id"])

        if product["picture"]:
            ET.SubElement(offer, "picture").text = product["picture"]

        ET.SubElement(offer, "url").text = product["url"]
        ET.SubElement(offer, "description").text = product["description"]

    xml_bytes = ET.tostring(root, encoding="utf-8")
    pretty_xml = minidom.parseString(xml_bytes).toprettyxml(
        indent="  ",
        encoding="utf-8"
    )

    with open(output_file, "wb") as f:
        f.write(pretty_xml)

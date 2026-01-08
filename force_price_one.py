# force_price_one.py

from xml.etree.ElementTree import parse

FILENAME = "feed.yml"


def set_all_prices_to_one():
    tree = parse(FILENAME)
    root = tree.getroot()

    count = 0

    # Ищем все теги <price>
    for price in root.iter("price"):
        price.text = "1"
        count += 1

    tree.write(
        FILENAME,
        encoding="utf-8",
        xml_declaration=True
    )

    print(f"✅ Готово! Цены изменены у {count} товаров (price = 1)")


if __name__ == "__main__":
    set_all_prices_to_one()

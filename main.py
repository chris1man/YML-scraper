from scraper import parse_products
from yml import generate_xml
from settings import OUTPUT_FILE


def main():
    print("🔍 Парсим главную страницу MAKI...")

    products, categories = parse_products()

    print(f"📦 Категорий: {len(categories)}")
    print(f"🛍 Товаров: {len(products)}")

    if not products:
        print("❌ Товары не найдены — проверь HTML")
        return

    generate_xml(products, categories, OUTPUT_FILE)

    print(f"✅ XML-фид создан: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

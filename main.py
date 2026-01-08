# main.py

from scraper import get_product_links, parse_product
from yml import generate_yml


def main():
    print("🔍 Получаем список товаров...")
    links = get_product_links()

    print(f"Найдено товаров: {len(links)}")
    print("Пример ссылок:", links[:3])

    products = []

    for link in links:
        print(f"Парсим: {link}")
        products.append(parse_product(link))

    print("📝 Генерируем YML...")
    generate_yml(products)

    print("✅ Готово! Файл feed.yml создан")


if __name__ == "__main__":
    main()

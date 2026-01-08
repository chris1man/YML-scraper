from scraper import get_product_links, parse_product
from yml import generate_yml

print("🔍 Получаем список товаров...")
links = get_product_links()
print(f"Найдено товаров: {len(links)}")

products = []

for link in links:
    print("Парсим:", link)
    product = parse_product(link)
    if product:
        products.append(product)
print("📝 Генерируем XML...")
generate_yml(products)
print("✅ Готово! Файл feed.xml создан")

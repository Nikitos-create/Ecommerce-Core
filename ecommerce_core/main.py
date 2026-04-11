from ecommerce_core.models import Product, Category

# Примеры использования
category1 = Category("Electronics", "Гаджеты и техника")
product1 = Product("iPhone 15", "Смартфон", 99999.99, 10)
category1.add_product(product1)


if __name__ == "__main__":
    print("E-commerce Core ready!")
    # Тестовый код (опционально)
    cat = Category("Test", "Test")
    print(f"Категорий: {Category.category_count}")

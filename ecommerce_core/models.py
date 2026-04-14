class Product:
    def __init__(self, name: str, desc: str, price: float, qty: int):
        self.name = name
        self.desc = desc
        self.price = price
        self.qty = qty


class Category:
    # Атрибуты класса по заданию
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.products = []
        self.category_count = Category.category_count  # ← 1
        Category.category_count += 1

    def add_product(self, product: Product):
        """Добавляет Product в категорию"""
        self.products.append(product)
        Category.product_count += 1

    @classmethod  # ← 4 ПРОБЕЛА!
    def load_ecommerce_data(cls):  # ← 4 ПРОБЕЛА!
        """🆕 Загрузка тестовых данных — метод класса!"""
        electronics = cls("Electronics", "Гаджеты и техника")
        electronics.add_product(Product("iPhone 15", "Смартфон", 99999.99, 10))
        electronics.add_product(Product("MacBook", "Ноутбук", 199999.99, 5))
        return electronics

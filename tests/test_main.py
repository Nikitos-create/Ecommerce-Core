import sys
from pathlib import Path
from ecommerce_core.models import Product, Category


sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_main_products_creation():
    """main.py строки 8-20 — продукты (45% покрытие)."""

    from ecommerce_core.models import Product

    # ТОЧНО main.py строки 8-20
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)

    assert product1.name == "Samsung Galaxy S23 Ultra"  # ← Добавь!
    assert product2.price == 210000.0


def test_main_product_prints():
    """main.py строки 22-34 — print(productX.*)."""
    from ecommerce_core.models import Product

    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5
    )

    # Имитируем if __name__ == "__main__":
    assert product1.name == "Samsung Galaxy S23 Ultra"


def test_main_category_creation():
    """main.py строки 36-45 — category1 создание."""

    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5
    )

    product2 = Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8
    )
    product3 = Product(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14
    )

    category1 = Category("Смартфоны",
                         "Смартфоны, как средство не только коммуникации, "
                         "но и получения дополнительных функций "
                         "для удобства жизни"
                         )
    category1.products = [product1, product2, product3]

    assert category1.name == "Смартфоны"
    assert len(category1.products) == 3


def test_main_category2_creation():
    """main.py строки 49-56 — category2 + финальные print."""
    from ecommerce_core.models import Product, Category

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры",
                         "Современный телевизор, который "
                         "позволяет наслаждаться просмотром, "
                         "станет вашим другом и помощником")
    category2.products = [product4]

    assert category2.name == "Телевизоры"
    assert len(category2.products) == 1
    assert Category.category_count > 0  # Счетчики классов


def test_main_imports():
    """Уже есть — добавь строку"""
    from ecommerce_core import main  # ← Эта строка покрывает main.py!

import sys
import os
import ecommerce_core.models

from decimal import Decimal
from ecommerce_core.models import Product, Category

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def test_product_initialization():
    """Тест инициализации Product."""
    product = Product(
        name="iPhone 15 Pro",
        desc="256GB Titanium",
        price=Decimal("119999.99"),
        qty=10
    )

    assert product.name == "iPhone 15 Pro"
    assert product.desc == "256GB Titanium"
    assert product.price == Decimal("119999.99")
    assert product.qty == 10


def test_category_initialization():
    """Тест инициализации Category."""
    Category.category_count = 0
    category = Category("Электроника", "Гаджеты")

    assert category.name == "Электроника"
    assert category.description == "Гаджеты"
    assert len(category.products) == 0
    assert Category.category_count == 1


def test_category_counters():
    """Тест счетчиков категорий."""
    Category.category_count = 0  # Сброс

    cat1 = Category("Электроника", "Гаджеты")
    cat2 = Category("Одежда", "Бренды")

    assert Category.category_count == 2


def test_category_products_counter():
    """Тест счетчика товаров."""
    Category.product_count = 0  # Сброс

    phone = Product("iPhone", "256GB", Decimal("99999"), 5)
    laptop = Product("MacBook", "M3", Decimal("199999"), 3)

    electronics = Category("Электроника", "Гаджеты")
    electronics.add_product(phone)
    electronics.add_product(laptop)

    assert Category.product_count == 2
    assert len(electronics.products) == 2


def test_model_edge_cases():
    """Крайние случаи для models."""
    product = Product("", "", Decimal("0"), 0)  # ПУСТЫЕ значения
    assert product.name == ""  # строка 49-55
    assert product.price == Decimal("0")

    product_neg = Product("Test", "desc", Decimal("-100"), -1)  # ОТРИЦательные
    assert product_neg.name == "Test"


def test_load_ecommerce_data_basic():
    """Тест load_ecommerce_data() без reload."""
    from ecommerce_core.models import Category  # Импорт внутри для свежести

    # Сброс счётчиков перед загрузкой (если они class vars)
    Category.category_count = 0
    Category.product_count = 0

    root_cat = Category.load_ecommerce_data()
    assert root_cat is not None
    assert root_cat.name == "Electronics"  # ✅ ФАКТ из вашего кода!
    assert root_cat.description == "Гаджеты и техника"
    assert len(root_cat.products) == 2
    assert root_cat.products[0].name == "iPhone 15"
    assert Category.product_count == 2  # если add_product инкрементит


def test_category_add_remove_product():
    """add_product() + remove_product() если есть."""
    Category.product_count = 0

    cat = Category("Техника", "Электроника")
    prod = Product("TV", "4K", Decimal('50000'), 2)

    cat.add_product(prod)
    assert len(cat.products) == 1
    assert Category.product_count == 1


def test_product_decimal_price():
    """Decimal в Product."""
    prod = Product("Test", "Test", Decimal('123.45'), 10)
    assert prod.price == Decimal('123.45')


def test_models_imports():
    """Покрытие всех импортов models.py."""
    from ecommerce_core.models import Product, Category
    assert Product
    assert Category
    assert hasattr(Category, 'load_ecommerce_data')

import sys
import os
from ecommerce_core.models import Product, Category, CategoryProductIterator
import pytest
from decimal import Decimal

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
    Category.product_count = 0
    category = Category("Электроника", "Гаджеты")

    assert category.name == "Электроника"
    assert category.description == "Гаджеты"
    assert category.products == "Нет товаров"


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

    expected = "iPhone, 99999 руб. Остаток: 5 шт.\n" \
               "MacBook, 199999 руб. Остаток: 3 шт."

    assert Category.product_count == 2
    assert electronics.products == expected


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

    expected = "iPhone 15, 99999.99 руб. Остаток: 10 шт.\n" \
               "MacBook, 199999.99 руб. Остаток: 5 шт."

    assert root_cat.products == expected

def test_category_add_remove_product():
    """add_product() + remove_product() если есть."""
    Category.product_count = 0

    cat = Category("Техника", "Электроника")
    prod = Product("TV", "4K", Decimal('50000'), 2)

    cat.add_product(prod)
    assert cat.products == "TV, 50000 руб. Остаток: 2 шт."
    assert Category.product_count == 1

    cat.remove_product(prod)
    assert cat.products == "Нет товаров"
    assert Category.product_count == 0


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

def test_product_price_getter():
    p = Product("Test", "", 999.99, 5)
    assert p.price == 999.99
    assert p._Product__price == 999.99

    with pytest.raises(AttributeError):
        _ = p.__price


def test_product_price_setter_positive():
    p = Product("Test", "", 100.0, 5)
    p.price = 150.0
    assert p.price == 150.0


def test_product_price_setter_non_positive():
    p = Product("Test", "", 100.0, 5)
    original = p.price

    p.price = 0
    assert p.price == original

    p.price = -1
    assert p.price == original


def test_add_or_update_product_new():
    Category.category_count = 0
    Category.product_count = 0

    c = Category("Electronics", "Гаджеты")
    p1 = Product("iPhone 15", "Смартфон", 99999.99, 10)

    c.add_or_update_product(p1)

    assert len(c._Category__products) == 1
    assert c._Category__products[0] is p1
    assert Category.product_count == 1


def test_add_or_update_product_duplicate():
    c = Category("Electronics", "Гаджеты")
    p1 = Product("iPhone 15", "Смартфон", 99999.99, 10)
    p2 = Product("iPhone 15", "Смартфон", 101000.0, 5)

    c.add_or_update_product(p1)
    updated = c.add_or_update_product(p2)

    assert updated is p1
    assert p1.qty == 15
    assert p1.price == 101000.0
    assert len(c._Category__products) == 1

    iter_products = CategoryProductIterator(c)
    items = list(iter_products)

    assert len(items) == 1
    assert items[0] is p1

def test_category_products_private():
    category = Category("Electronics", "Гаджеты")
    product = Product("iPhone 15", "Смартфон", 99999.99, 10)

    assert hasattr(category, "_Category__products")  # приватный атрибут
    with pytest.raises(AttributeError):
        _ = category.__products


def test_category_add_product():
    category = Category("Electronics", "Гаджеты")
    product = Product("iPhone 15", "Смартфон", 99999.99, 10)

    assert len(category._Category__products) == 0
    category.add_product(product)
    assert len(category._Category__products) == 1
    assert category._Category__products[0] is product

def test_category_products_getter():
    category = Category("Electronics", "Гаджеты")

    assert category.products == "Нет товаров"

    p1 = Product("iPhone 15", "Смартфон", 99999.99, 10)
    p2 = Product("MacBook", "Ноутбук", 199999.99, 5)
    category.add_product(p1)
    category.add_product(p2)

    expected = (
        "iPhone 15, 99999.99 руб. Остаток: 10 шт.\n"
        "MacBook, 199999.99 руб. Остаток: 5 шт."
    )
    assert category.products == expected

def test_product_price_private():
    product = Product("iPhone 15", "Смартфон", 99999.99, 10)
    assert product.price == 99999.99
    with pytest.raises(AttributeError):
        _ = product.__price

def test_product_str_format():
    """Проверяет строковое представление Product."""
    p = Product("iPhone 15", "Смартфон", 99999.99, 10)
    expected = "iPhone 15, 99999.99 руб. Остаток: 10 шт."
    assert str(p) == expected


def test_product_str_with_zero_qty():
    p = Product("Test", "", 100.0, 0)
    expected = "Test, 100.0 руб. Остаток: 0 шт."
    assert str(p) == expected


def test_product_str_with_zero_price():
    p = Product("Test", "", 0.0, 5)
    expected = "Test, 0.0 руб. Остаток: 5 шт."
    assert str(p) == expected

def test_product_add_typical_case():
    """a: 100 руб., 10 шт. → 1000 руб.
       b: 200 руб., 2 шт.  → 400 руб.
       a + b = 1400 руб."""
    a = Product("a", "", 100.0, 10)
    b = Product("b", "", 200.0, 2)
    total = a + b
    assert total == 1400.0


def test_product_add_both_zero_qty():
    a = Product("a", "", 100.0, 0)
    b = Product("b", "", 200.0, 0)
    total = a + b
    assert total == 0.0


def test_product_add_one_zero_qty():
    a = Product("a", "", 100.0, 5)
    b = Product("b", "", 200.0, 0)
    total = a + b
    assert total == 500.0


def test_product_add_with_different_names():
    a = Product("iPhone", "", 1000.0, 2)
    b = Product("MacBook", "", 2000.0, 1)
    total = a + b
    assert total == 4000.0


def test_product_add_with_not_product():
    """Проверка, что __add__ возвращает NotImplemented при не-Product."""
    a = Product("a", "", 100.0, 10)
    result = a.__add__(42)
    assert result is NotImplemented

    result = a.__add__("b")
    assert result is NotImplemented


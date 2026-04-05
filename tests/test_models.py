import tempfile
import json
from pathlib import Path
from decimal import Decimal
from ecommerce_core.models import Product, Category, load_ecommerce_data


def test_product_initialization():
    """Тест инициализации Product."""
    product = Product(
        name="iPhone 15 Pro",
        description="256GB Titanium",
        price=Decimal("119999.99"),
        quantity=10
    )

    assert product.name == "iPhone 15 Pro"
    assert product.description == "256GB Titanium"
    assert product.price == Decimal("119999.99")
    assert product.quantity == 10


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
    assert cat1.category_count == 2
    assert cat2.category_count == 2


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
    """~строки 49-75 — load_ecommerce_data() полный тест."""
    # Создаем тестовый JSON
    import ecommerce_core.models

    Category.category_count = 0
    Category.product_count = 0

    test_data = {
        "categories": [{"name": "Техника", "description": "Электроника"}],
        "products": [
            {
                "name": "TV",
                "description": "4K",
                "price": 50000,
                "quantity": 2,
                "category": "Техника"
            }
        ]
    }

    with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False
    ) as f:
        json.dump(test_data, f)
        json_path = Path(f.name)

    try:
        root_cat, all_cats = (
             ecommerce_core.models.load_ecommerce_data(json_path)
        )

        assert root_cat is not None
        assert len(all_cats) == 1
        assert all_cats[0].name == "Техника"
        assert len(all_cats[0].products) == 1
        assert all_cats[0].products[0].name == "TV"
        assert all_cats[0].product_count == 1
        assert Category.category_count == 1  # ← Счетчики!
    finally:
        json_path.unlink()  # Удаляем файл


def test_load_ecommerce_data_empty():
    """Пустой JSON."""
    empty_data = {"categories": [], "products": []}

    with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False
    ) as f:
        json.dump(empty_data, f)
        json_path = Path(f.name)

    try:
        root_cat, all_cats = load_ecommerce_data(json_path)
        assert root_cat is None
        assert len(all_cats) == 0
    finally:
        json_path.unlink()


def test_category_add_remove_product():
    """add_product() + remove_product() если есть."""
    Category.product_count = 0

    cat = Category("Техника", "Электроника")
    prod = Product("TV", "4K", Decimal('50000'), 2)

    cat.add_product(prod)
    assert len(cat.products) == 1
    assert Category.product_count == 1

    # Если есть remove_product — протестируй
    # cat.remove_product(prod)


def test_product_decimal_price():
    """Decimal в Product."""
    prod = Product("Test", "Test", Decimal('123.45'), 10)
    assert prod.price == Decimal('123.45')


def test_models_imports():
    """Покрытие всех импортов models.py."""
    from ecommerce_core.models import load_ecommerce_data, Product, Category
    assert load_ecommerce_data
    assert Product
    assert Category

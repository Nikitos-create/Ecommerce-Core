import io
import sys
import os
from ecommerce_core.models import (Product, Category,
                                   BaseProduct,
                                   BaseOrderable,
                                   PrintCreationMixin,
                                   Order,
                                   CategoryProductIterator,
                                   Smartphone, LawnGrass,
                                   Category)
import pytest
from io import StringIO
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def test_product_initialization():
    """Тестирование инициализации Product."""
    product = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5
    )

    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_category_initialization():
    Category.category_count = 0

    # Создаём одну категорию
    category = Category("Test Category", "Описание тестовой категории")

    # Проверяем, что счётчик увеличился ровно на 1
    assert Category.category_count == 1, f"Ожидалось 1, получено {Category.category_count}"


def test_category_add_product():
    """Тестирование add_product."""
    category = Category("Телевизоры", "Современный телевизор")
    product = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)

    category.add_product(product)

    assert Category.product_count == 1

    # Проверяем результат через геттер products (он тоже использует __products)
    result = category.products
    assert "Смартфон" in result
    assert "50000 руб." in result


@pytest.fixture(autouse=True)
def clean_categories():
    """Очищает состояние категорий перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0

def test_category_count():
    """Тестирование category_count."""

    # Убедимся, что изначально счётчик равен 0
    assert Category.category_count == 0

    # Создаём и сохраняем категории
    Category("Смартфоны", "Смартфоны")
    Category("Телевизоры", "Телевизоры")

    # Проверяем, что счётчик обновился до 2
    assert Category.category_count == 2


def test_category_products_counter():
    """Тест счётчика товаров."""
    Category.product_count = 0

    print(f"Начальное значение (после сброса): {Category.product_count}")

    # Создаём категорию
    electronics = Category("Электроника", "Гаджеты")

    # Проверяем начальное состояние — через внутренний список _products
    assert electronics.products == 'Нет товаров'
    assert Category.product_count == 0, f"Начальный счётчик должен быть 0, но был {Category.product_count}"

    # Создаём товары с корректными типами данных
    phone = Product("iPhone", "256GB", 99999, 5)
    laptop = Product("MacBook", "M3", 199999, 3)

    # Добавляем товары
    electronics.add_product(phone)
    electronics.add_product(laptop)

    result = electronics.products
    assert "iPhone" in result, "iPhone должен быть в отформатированной строке"
    assert "MacBook" in result, "MacBook должен быть в отформатированной строке"

    # Проверяем счётчик продуктов
    assert Category.product_count == 2, f"Счётчик должен быть 2, но был {Category.product_count}"

def test_load_ecommerce_data_basic():
    """Тест load_ecommerce_data() без reload."""
    from ecommerce_core.models import Category, Product

    # Сброс счётчиков перед загрузкой
    Category.category_count = 0
    Category.product_count = 0


    # Загружаем данные — получаем корневую категорию
    root_cat = Category.load_ecommerce_data()

    # Проверяем, что вернули категорию
    assert isinstance(root_cat, Category)

    # Проверяем название и описание категории
    assert root_cat.name == "Electronics"
    assert root_cat.description == "Гаджеты и техника"

    # Проверяем количество товаров через внутренний список (с учётом name mangling)
    internal_products = getattr(root_cat, '_Category__products')
    assert len(internal_products) == 2, "В категории должно быть 2 товара"

    # Ищем товар iPhone 15
    iphone = next((p for p in internal_products if p.name == "iPhone 15"), None)
    assert iphone is not None, "Товар iPhone 15 не найден в категории"

    # Проверяем корректность данных iPhone 15
    assert iphone.price == 99999.99
    assert iphone.quantity == 10

    # Ищем товар MacBook
    macbook = next((p for p in internal_products if p.name == "MacBook"), None)
    assert macbook is not None, "Товар MacBook не найден в категории"

    # Проверяем корректность данных MacBook
    assert macbook.price == 199999.99
    assert macbook.quantity == 5

    # Дополнительно: проверяем, что счётчик товаров увеличился на 2
    assert Category.product_count == 2, f"Счётчик товаров должен быть 2, но был {Category.product_count}"

def test_models_imports():
    """Покрытие всех импортов models.py."""
    from ecommerce_core.models import Product, Category
    assert Product
    assert Category
    assert hasattr(Category, 'load_ecommerce_data')


def test_product_price_getter():
    p = Product("Test", "", 999.99, 5)
    assert p.price == 999.99
    assert p._BaseProduct__price == 999.99

    with pytest.raises(AttributeError):
        _ = p.__price


def test_product_price_setter_positive():
    p = Product("Test", "", 100.0, 5)
    p.price = 150.0
    assert p.price == 150.0


def test_product_price_setter_non_positive():
    product = Product("TV", "Телевизор", 100.0, 2)

    # Проверяем, что установка неположительной цены вызывает исключение
    with pytest.raises(ValueError, match="Цена должна быть положительной"):
        product.price = -50.0

    # Убеждаемся, что цена осталась прежней
    assert product.price == 100.0


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
    assert p1.quantity == 15
    assert p1.price == 101000.0
    assert len(c._Category__products) == 1

    iter_products = CategoryProductIterator(c)
    items = list(iter_products)

    assert len(items) == 1
    assert items[0] is p1


def test_category_products_private():
    category = Category("Electronics", "Гаджеты")
    product = Product("iPhone 15", "Смартфон", 99999.99, 10)

    category.add_product(product)

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

    print(f"Тип category.products: {type(category.products)}")
    print(f"Значение category.products: {category.products}")

    assert category.products == "Нет товаров"

    p1 = Product("iPhone 15", "Смартфон", 99999.99, 10)
    p2 = Product("MacBook", "Ноутбук", 199999.99, 5)
    category.add_product(p1)
    category.add_product(p2)

    expected = (
        "iPhone 15, 99999.99 руб. Остаток: 10 шт.\n"
        "MacBook, 199999.99 руб. Остаток: 5 шт."
    )
    print(f"Ожидаемое: {expected}")
    print(f"Фактическое: {category.products}")
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


def test_smartphone_inheritance():
    s = Smartphone(
        "iPhone 15 Pro",
        "256GB Titanium",
        ("119999.99"),
        10,
        "iOS"
    )
    assert s.name == "iPhone 15 Pro"
    assert s.quantity == 10

    assert "256GB Titanium" in str(s), "Описание должно быть в строковом представлении"

    # Проверяем основные компоненты строки
    assert "iPhone 15 Pro" in str(s)
    assert "119999.99" in str(s)
    assert "Остаток: 10" in str(s)

def test_lawngrass_inheritance():
    lg = LawnGrass(
        "Газонная трава Premium",
        "Высокоурожайная",
        ("999.99"),
        100,
        country="Россия",
    )
    assert lg.country == "Россия"

def test_product_add_same_type():
    a = Product("Test A", "", 100.0, 10)
    b = Product("Test B", "", 200.0, 5)
    total = a + b
    assert total == 2000.0


def test_category_add_valid_product():
    c = Category("Электроника", "Гаджеты")
    p = Product("Test", "", 100.0, 10)
    s = Smartphone("Sm A", "", 1000.0, 5, "A15")

    c.add_product(p)
    c.add_product(s)
    assert len(c._Category__products) == 2


def test_category_add_invalid_type_raises():
    c = Category("Электроника", "Гаджеты")

    with pytest.raises(TypeError):
        c.add_product("not a product")

    with pytest.raises(TypeError):
        c.add_product(42)


# === 1. Тест на BaseProduct (абстрактность) ===
def test_base_product_is_abstract():
    """BaseProduct нельзя инстанциировать напрямую."""
    with pytest.raises(TypeError):
        BaseProduct("test", "desc", 100.0, 10)


# === 2. Тест, что Product наследует BaseProduct и миксин ===
def test_product_inherits_base_product_and_mixin():
    """Product наследует BaseProduct и PrintCreationMixin."""
    assert issubclass(Product, BaseProduct), "Product должен наследоваться от BaseProduct"
    assert issubclass(Product, PrintCreationMixin), "Product должен наследоваться от PrintCreationMixin"

# === 4. Тест на __repr__ от PrintCreationMixin ===
def test_print_creation_mixin_repr():
    """У Product корректно работает __repr__ от миксина."""
    p = Product("Тест", "описание", 100.0, 10)
    expected = "Product('Тест', 'описание', 100.0, 10)"
    assert repr(p) == expected


# === 5. Тест, что BaseProduct обязывает реализовать __str__ ===
def test_product_implements_baseproduct_str():
    """Product реализует абстрактный __str__ от BaseProduct."""
    p = Product("Тест", "описание", 100.0, 10)
    s = str(p)
    assert "Тест" in s
    assert "100.0 руб." in s
    assert "Остаток: 10 шт." in s


# === 6. Тест, что BaseProduct обязывает price как @property ===
def test_product_implements_baseproduct_price_property():
    """BaseProduct требует price как свойство; у Product оно работает."""
    p = Product("Тест", "описание", 100.0, 10)
    assert p.price == 100.0


# === 7. Тест price.setter с подтверждением снижения ===
def test_product_price_setter_with_confirmation(monkeypatch):
    """При снижении цены спрашивает подтверждение."""
    p = Product("Тест", "описание", 100.0, 10)

    # Подменяем input
    inputs = ["y"]

    def fake_input(*args, **kwargs):
        return inputs.pop(0)

    monkeypatch.setattr("builtins.input", fake_input)

    # Снижаем цену — подтверждаем
    p.price = 90.0
    assert p.price == 90.0

# === 8. Тест, что BaseProduct обязывает __add__ ===
def test_product_implements_baseproduct_add():
    """Product реализует абстрактный __add__ от BaseProduct."""
    p1 = Product("Тест1", "desc", 100.0, 10)
    p2 = Product("Тест2", "desc", 50.0, 5)

    total = p1 + p2
    expected = 100.0 * 10 + 50.0 * 5  # 1000 + 250
    assert total == 1250.0

# === 9. Тесты для наследников Product: Smartphone и LawnGrass ===
def test_smartphone_is_subclass_of_product():
    """Smartphone наследует Product (и через него — BaseProduct)."""
    s = Smartphone(
        "iPhone",
        "описание",
        100000.0,
        1,
        "high",
    )
    assert isinstance(s, Product)


def test_lawngrass_is_subclass_of_product():
    """LawnGrass наследует Product (и через него — BaseProduct)."""
    lawn = LawnGrass(
        "Газонная трава", "описание", 1000.0, 20,3)
    assert isinstance(lawn, Product)


# === 10. Тесты для BaseOrderable и Order ===
def test_baseorderable_is_abstract():
    """BaseOrderable нельзя инстанциировать напрямую."""
    with pytest.raises(TypeError):
        BaseOrderable("test", "desc")


def test_order_inherits_baseorderable():
    """Order наследует BaseOrderable."""
    product = Product("Тест", "desc", 100.0, 10)
    order = Order(product, 3)
    assert isinstance(order, BaseOrderable)


def test_order_item_count():
    """item_count у Order — это количество товаров в заказе."""
    product = Product("Тест", "desc", 100.0, 10)
    order = Order(product, 5)
    assert order.item_count == 5


def test_order_total_cost():
    """total_cost у Order — это цена товара × количество."""
    product = Product("Тест", "desc", 100.0, 10)
    order = Order(product, 3)
    assert order.total_cost == 100.0 * 3  # 300.0

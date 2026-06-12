from abc import ABC, abstractmethod


class BaseOrderable(ABC):
    """
    Общий базовый класс для заказа и категории.
    Определяет единый базовый интерфейс для объектов,
    которые можно "заказывать" и учитывать по количеству и стоимости.
    """

    @abstractmethod
    def __init__(self, name: str, description: str) -> None:
        pass

    @property
    @abstractmethod
    def item_count(self) -> int:
        return 0

    @property
    @abstractmethod
    def total_cost(self) -> float:
        return 0.0


# === 1. Задание 1 — абстрактный базовый класс BaseProduct ===
class BaseProduct(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int):
        self.__name = name
        self.__description = description
        self.__price = price
        self.__quantity = quantity

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str) -> None:
        self.__description = value

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Цена должна быть положительной")
        self.__price = value

    @property
    def quantity(self) -> int:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        self.__quantity = value

    @abstractmethod
    def get_info(self) -> str:
        pass

    def __str__(self) -> str:
        if self.__quantity == 0:
            return f"{self.__name}, {self.__price} руб. Остаток: 0 шт."
        return (f"{self.__name}, {self.__price} руб. "
                f"Остаток: {self.__quantity} шт.")


# === 2. Задание 2 — миксин PrintCreationMixin ===
class PrintCreationMixin:
    """
    Миксин: при создании объекта печатает в консоль,
    от какого класса и с какими параметрами он был создан.
    """

    def __init__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        args_str = ', '.join(repr(arg) for arg in args)
        if kwargs:
            kwargs_str = ', '.join(f'{k}={v!r}' for k, v in kwargs.items())
            line = f"{class_name}({args_str}, {kwargs_str})"
        else:
            line = f"{class_name}({args_str})"

        print(line)

        self._init_args = args
        self._init_kwargs = kwargs

    def __repr__(self) -> str:
        args_str = ', '.join(repr(arg) for arg in self._init_args)
        if self._init_kwargs:
            kwargs_str = ', '.join(
                f'{k}={v!r}' for k, v in self._init_kwargs.items()
            )
            return f"{self.__class__.__name__}({args_str}, {kwargs_str})"
        else:
            return f"{self.__class__.__name__}({args_str})"


class Product(BaseProduct, PrintCreationMixin):
    def __init__(self, name, description, price, quantity):
        super().__init__(name, description, price, quantity)
        PrintCreationMixin.__init__(self, name, description, price, quantity)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def get_info(self) -> str:
        return str(self)

    def __add__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price * self.quantity + other.price * other.quantity


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("В категорию можно "
                            "добавлять только "
                            "объекты Product")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        if not self.__products:
            return 'Нет товаров'
        formatted_products = []
        for product in self.__products:
            formatted_products.append(
                f"{product.name}, {product.price} руб. "
                f"Остаток: {product.quantity} шт."
            )
        return '\n'.join(formatted_products)

    @classmethod
    def load_ecommerce_data(cls):
        electronics = cls("Electronics", "Гаджеты и техника")
        electronics.add_product(Product("iPhone 15", "Смартфон", 99999.99, 10))
        electronics.add_product(Product("MacBook", "Ноутбук", 199999.99, 5))
        return electronics

    @classmethod
    def new_product(cls, data: dict) -> 'Product':
        """
        Создаёт Product или обновляет существующий:
        - Если товар есть → qty += qty, price = max(price)
        - Если нет → новый Product
        """
        # ✅ Создаём новый
        return Product(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"]
        )

    def add_or_update_product(self, product: 'Product'):
        # 🔍 Ищем дубликат по имени
        for existing in self.__products:
            if existing.name.lower() == product.name.lower():
                existing.quantity += product.quantity
                existing.price = max(existing.price, product.price)
                return existing

        self.__products.append(product)
        Category.product_count += 1
        return product


class CategoryProductIterator:
    """Итератор по товарам одной категории."""

    def __init__(self, category: Category):
        # приватный __products доступен через name mangling
        self.__products = category._Category__products
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> 'Product':
        if self._index >= len(self.__products):
            raise StopIteration

        product = self.__products[self._index]
        self._index += 1
        return product


class Smartphone(Product):
    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            os: str):
        super().__init__(name, description, price, quantity)
        self.__os = os

    @property
    def os(self) -> str:
        return self.__os

    def __str__(self) -> str:
        return (
            f"{self.name} {self.description} ,"
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )

    def get_total_price(self) -> float:
        return self.price * self.quantity

    def get_info(self) -> str:
        return (f"{self.name}: "
                f"{self.model}, {self.memory}GB, "
                f"{self.color}, {self.price} руб.")


class LawnGrass(Product):
    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            country: str):
        super().__init__(name, description, price, quantity)
        self.__country = country

    @property
    def country(self) -> str:
        return self.__country

    def __str__(self) -> str:
        return (
            f"{self.name}, {self.country}, "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )

    def get_total_price(self) -> float:
        return self.price * self.quantity

    def get_info(self) -> str:
        return (f"{self.name}: {self.season}, "
                f"рост {self.growth_rate}м/год, "
                f"{self.price} руб.")


class Order(BaseOrderable):
    """
    Класс заказа, в котором указан один товар, количество и итоговая стоимость.
    """

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        super().__init__(product.name, product.description)

    @property
    def name(self) -> str:
        return self.product.name

    @property
    def description(self) -> str:
        return self.product.description

    @property
    def item_count(self) -> int:
        return self.quantity

    @property
    def total_cost(self) -> float:
        return self.product.price * self.quantity

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
    """
    Базовый абстрактный класс для всех продуктов.
    Общая функциональность: название, описание, цена, количество.
    """

    @abstractmethod
    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int
    ) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other: 'BaseProduct') -> float:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float) -> None:
        pass


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


class Product(PrintCreationMixin, BaseProduct):
    """
    Конкретный класс продукта, наследуется от BaseProduct и миксина.
    """

    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int
    ):
        super().__init__(name, description, price, quantity)

        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'BaseProduct') -> float:
        """Сложение товаров по общей стоимости на складе."""
        if not isinstance(other, BaseProduct):
            return NotImplemented
        if type(self) is not type(other):
            raise TypeError(
                "Можно складывать только товары "
                "из одинакового класса продуктов"
            )

        self_value = self.price * self.quantity
        other_value = other.price * other.quantity
        return self_value + other_value

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if new_price < self.__price:
            confirm = input(
                f"Цена снижается с {self.__price} до {new_price}. "
                f"Подтвердить? (y/n): "
            )
            if confirm.lower() != 'y':
                print("Изменение цены отменено")
                return
        self.__price = new_price

    @classmethod
    def load_ecommerce_data(cls):
        electronics = cls("Electronics", "Гаджеты и техника")
        electronics.add_product(cls("iPhone 15", "Смартфон", 99999.99, 10))
        electronics.add_product(cls("MacBook", "Ноутбук", 199999.99, 5))
        return electronics


class Category:
    # Атрибуты класса по заданию
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

    def add_product(self, product: 'Product') -> None:
        """Добавляет Product в категорию"""
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять "
                            "только объекты Product или его наследников")

        self.__products.append(product)
        Category.product_count += 1

    def remove_product(self, product: 'Product'):
        if product in self.__products:
            self.__products.remove(product)
            Category.product_count -= 1

    @property
    def products_count(self):
        """Необязательно, но если хочется числовой счётчик"""
        return len(self.__products)

    @property
    def products(self) -> str:
        """
        Геттер для приватного атрибута __products.
        Возвращает строку в формате:
            "Название, X руб. Остаток: X шт.\n"
        для всех продуктов.
        """
        if not self.__products:
            return "Нет товаров"

        lines = []
        for product in self.__products:
            line = (f"{product.name}, {product.price} руб. "
                    f"Остаток: {product.quantity} шт.")
            lines.append(line)

        return "\n".join(lines)

    def __str__(self) -> str:
        """
        Возвращает строку в формате:
        'Название категории, количество продуктов: X шт.'
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def get_quantity_summary(self) -> str:
        """
        Возвращает строку вида:
        'Название категории, количество продуктов: 150 шт.'
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @classmethod
    def load_ecommerce_data(cls):
        """Загрузка тестовых данных — метод класса!"""
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
            desc=data["desc"],
            price=data["price"],
            quantity=data["quantity"]
        )

    def add_or_update_product(self, product: 'Product'):
        # 🔍 Ищем дубликат по имени
        for existing in self.__products:
            if existing.name.lower() == product.name.lower():
                existing.qty += product.quantity
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
        efficiency: str,
        model: str,
        memory: int,
        color: str
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        return (
            f"{self.name} {self.model}, {self.efficiency}, {self.memory} ГБ, "
            f"{self.color}, {self.price} руб. Остаток: {self.quantity} шт."
        )


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        return (
            f"{self.name}, {self.country}, "
            f"период прорастания: {self.germination_period} дней, "
            f"{self.color}, {self.price} руб. Остаток: {self.quantity} шт."
        )


class Order(BaseOrderable):
    """
    Класс заказа, в котором указан один товар, количество и итоговая стоимость.
    """

    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        super().__init__(product.name, product.desc)

    @property
    def name(self) -> str:
        return self.product.name

    @property
    def description(self) -> str:
        return self.product.desc

    @property
    def item_count(self) -> int:
        return self.quantity

    @property
    def total_cost(self) -> float:
        return self.product.price * self.quantity

class Product:
    def __init__(self, name: str, desc: str, price: float, qty: int):
        self.name = name
        self.desc = desc
        self.__price = price
        self.qty = qty

    @property
    def price(self) -> float:
        """Геттер: чтение цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """Сеттер: проверка цены"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:  # 🔍 Цена ПОНИЗИЛАСЬ!
            confirm = input(f"Цена снижается с {self.__price} до {new_price}. Подтвердить? (y/n): ")
            if confirm.lower() != 'y':  # ❌ НЕ 'y'
                print("Изменение цены отменено")
                return

        self.__price = new_price  # ✅ Устанавливаем!

    def __str__(self) -> str:
        """Строковое представление продукта в формате:
        'Название, X руб. Остаток: X шт.'
            """
        return f"{self.name}, {self.price} руб. Остаток: {self.qty} шт."

    def __add__(self, other: 'Product') -> float:
        """
        Сложение товаров: суммарная стоимость всех товаров на складе.
        Пример: 100*10 + 200*2 = 1400.
        """
        if not isinstance(other, Product):
            return NotImplemented

        self_value = self.price * self.qty
        other_value = other.price * other.qty
        return self_value + other_value

    @classmethod
    def load_ecommerce_data(cls):
        electronics = cls("Electronics", "Гаджеты и техника")
        electronics.add_product(Product("iPhone 15", "Смартфон", 99999.99, 10))
        electronics.add_product(Product("MacBook", "Ноутбук", 199999.99, 5))
        return electronics

class Category:
    # Атрибуты класса по заданию
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.__products = []
        Category.category_count += 1

    def add_product(self, product: 'Product'):
        """Добавляет Product в категорию"""
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
            line = f"{product.name}, {product.price} руб. Остаток: {product.qty} шт."
            lines.append(line)

        return "\n".join(lines)

    def __str__(self) -> str:
        """
        Возвращает строку в формате:
        'Название категории, количество продуктов: X шт.'
        """
        total_qty = sum(product.qty for product in self.__products)
        return f"{self.name}, количество продуктов: {total_qty} шт."

    def get_quantity_summary(self) -> str:
        """
        Возвращает строку вида:
        'Название категории, количество продуктов: 150 шт.'
        """
        total_qty = sum(product.qty for product in self.__products)
        return f"{self.name}, количество продуктов: {total_qty} шт."

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
            qty=data["qty"]
        )

    def add_or_update_product(self, product: 'Product'):
        # 🔍 Ищем дубликат по имени
        for existing in self.__products:
            if existing.name.lower() == product.name.lower():
                existing.qty += product.qty
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
        desc: str,
        price: float,
        qty: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str
    ):
        super().__init__(name, desc, price, qty)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        return (
            f"{self.name} {self.model}, {self.efficiency}, {self.memory} ГБ, "
            f"{self.color}, {self.price} руб. Остаток: {self.qty} шт."
        )

class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        desc: str,
        price: float,
        qty: int,
        country: str,
        germination_period: int,
        color: str
    ):
        super().__init__(name, desc, price, qty)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        return (
            f"{self.name}, {self.country}, всхожесть: {self.germination_period} дней, "
            f"{self.color}, {self.price} руб. Остаток: {self.qty} шт."
        )




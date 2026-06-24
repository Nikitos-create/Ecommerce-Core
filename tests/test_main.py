import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


#def test_main_products_creation():
#    """main.py строки 8-20 — продукты (45% покрытие)."""
#    from ecommerce_core.models import Product

#    product1 = Product(
 #       "Samsung Galaxy S23 Ultra",
  #      "256GB, Серый цвет, 200MP камера",
   #     180000.0,
   #     5
   # )
    #product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)

    # ✅ Только чтение (нет setter)
    #assert product1.name == "Samsung Galaxy S23 Ultra"
    #assert product2.name == "Iphone 15"
    #assert product2.price == 210000.0
    #assert product1.price == 180000.0
    #assert product1.quantity == 5
    #assert product2.quantity == 8


#def test_main_product_prints():
   # """main.py строки 22-34 — print(productX.*)."""
   # from ecommerce_core.models import Product

   # product1 = Product(
    #    "Samsung Galaxy S23 Ultra",
   #     "256GB, Серый цвет, 200MP камера",
    #    180000.0,
   #     5
   # )

    # ✅ Только чтение (нет setter)
  #  assert product1.name == "Samsung Galaxy S23 Ultra"
  #  assert product1.description == "256GB, Серый цвет, 200MP камера"
  #  assert product1.price == 180000.0
  #  assert product1.quantity == 5


#def test_main_category_creation():
 #   from ecommerce_core.models import Category

    # ✅ Добавлен products (required)
  #  category1 = Category(
     #   "Смартфоны",
     #   "Смартфоны, как средство не только коммуникации, "
      #  "но и получения дополнительных функций "
     #   "для удобства жизни",
      #  []  # ✅ products = пустой список
   # )
   # assert category1.name == "Смартфоны"
  #  assert category1.description == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
  #  assert category1.products == []


#def test_main_category2_creation():
   # """main.py строки 49-56 — category2 + финальные print."""
   # from ecommerce_core.models import Product, Category

  #  product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)

  #  # ✅ Добавлен products (required)
  #  category2 = Category(
  #      "Телевизоры",
   #     "Современный телевизор, который "
  #      "позволяет наслаждаться просмотром, "
  #      "станет вашим другом и помощником",
   #     []  # ✅ products = пустой список
  #  )

    # ✅ Используем append вместо add_product
 #   category2.products.append(product4)

  #  assert category2.name == "Телевизоры"
  #  assert category2.products == [product4]
   # assert len(category2.products) == 1

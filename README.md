# E-commerce Core

## Features:

* Category/Product модели
* JSON парсинг
* 16 тестов
* CI-ready



\### ✅ Реализованные возможности



\*\*Модели данных:\*\*

\- `Product` — товары с названием, описанием, ценой (`float`), количеством

\- `Category` — категории с авто-счетчиками:

&#x20; - `category\_count` — количество созданных категорий

&#x20; - `product\_count` — общее количество товаров

&#x20; - `add\_product()` — добавление товаров в категорию



\*\*Загрузка тестовых данных:\*\*

```python

root\_category = Category.load\_ecommerce\_data()

\# Electronics → iPhone 15, MacBook

```



Автор: Никита Рукин © 2026


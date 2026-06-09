# E-commerce Core
https://github.com/Nikitos-create/Ecommerce-Core
## Features:

* Category/Product модели
* JSON парсинг - сбор данных из JSON-файлов
* 16 тестов
* CI-ready



\### ✅ Реализованные возможности

Структурирование товаров по категориям с помощью классов Product, Category
Создание новых категорий товаров, подсчет количества товаров в категории

\*\*Модели данных:\*\*

\- `Product` — товары с названием, описанием, ценой (`float`), количеством

\- `Category` — категории с авто-счетчиками:

&#x20; - `category\_count` — количество созданных категорий

&#x20; - `product\_count` — общее количество товаров

&#x20; - `add\_product()` — добавление товаров в категорию



#### Установка и запуск

### 1. Клонируй репозиторий
```bash
git clone https://github.com/твой_username/ecommerce-core.git
cd ecommerce-core
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
# или
poetry install
```

### 3. Запуск проверок
```bash
PYTHONPATH=. pytest --cov=ecommerce_core tests/ -v
flake8 .
```



Автор: Никита Рукин © 2026
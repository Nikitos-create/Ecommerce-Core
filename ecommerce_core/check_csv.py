import csv

print("=== АНАЛИЗ orders_data.csv ===\n")
with open('orders_data.csv', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)
    print(f"Заголовок ({len(header)} колонок): {header}")

    for num, row in enumerate(reader, 1):
        if num > 3:
            break
        print(f"\nСтрока {num}: {row}")

print("\nСмотрим: в какой колонке employee_id (цифры 1, 2, 3... или 5)?")

# Домашнее задание № 5. Часть 1

import json
import csv

# Задание 5.1.1. ИНН из файла traders.txt
with open('traders.txt', 'r') as file:
    inn_list = [line.strip() for line in file if line.strip()]

print('Список ИНН из файла traders.txt:')
for inn in inn_list:
    print(inn)

# Задание 5.1.2. Организации из traders.json
with open('traders.json', 'r') as file:
    orgs = json.load(file)

# Задание 5.1.3. Фильтрация организаций по ИНН
filtered_orgs = []

print('\nНайденные по ИНН организации:')
for org in orgs:
    if org.get('inn') in inn_list:
        print(f'{org["short_name"]} | {org["inn"]} | {org["ogrn"]} | {org["address"]}')
        filtered = {
            'short_name': org.get('short_name'),
            'inn': org.get('inn'),
            'ogrn': org.get('ogrn'),
            'address': org.get('address')
        }
        filtered_orgs.append(filtered)

# Задание 5.1.4. CSV-файл с отфильтрованными организациями
with open('traders.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['short_name', 'inn', 'ogrn', 'address'], delimiter='|')
    writer.writeheader()
    writer.writerows(filtered_orgs)

print('\nСохранено в файл traders.csv')


# Домашнее задание № 5. Часть 2
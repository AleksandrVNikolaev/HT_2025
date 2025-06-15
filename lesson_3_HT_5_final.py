# Домашнее задание № 5. Часть 1
# Найдите информацию об организациях.
# a. Получите список ИНН из файла traders.txt.
# b. Найдите информацию об организациях с этими ИНН в файле traders.json.
# c. Сохраните информацию об ИНН, ОГРН и адресе организаций из файла traders.txt в файл traders.csv.

import json
import csv
import re


# Задание "а". ИНН из файла traders.txt
with open('traders.txt', 'r') as file:
    inn_list = [line.strip() for line in file if line.strip()]

print('Список ИНН из файла traders.txt:')
for inn in inn_list:
    print(inn)


# Задание "b_1". Организации из traders.json
with open('traders.json', 'r') as file:
    orgs = json.load(file)


# Задание "b_2". Фильтрация организаций по ИНН
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


# Задание "c". CSV-файл с отфильтрованными организациями
with open('traders.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['short_name', 'inn', 'ogrn', 'address'], delimiter='|')
    writer.writeheader()
    writer.writerows(filtered_orgs)

print('\nСохранено в файл traders.csv')


# Домашнее задание № 5. Часть 2
# Напишите регулярное выражение для поиска email-адресов в тексте. Для этого напишите функцию, которая принимает
# в качестве аргумента текст в виде строки и возвращает список найденных email-адресов или пустой список, если
# email-адреса не найдены.Используйте датасет на 1 000 сообщений из Единого федерального реестра сведений о банкротстве
# (ЕФРСБ) для практики. Найдите все email-адреса в датасете и соберите их в словарь, где ключом будет выступать
# ИНН опубликовавшего сообщение publisher_inn, а в значении будет храниться множество set() с email-адресами.
# Сохраните собранные данные в файл emails.json.


# 1) Загрузка JSON
with open('1000_efrsb_messages.json', 'r') as file:
    data = json.load(file)


# 2) Функция для поиска e-mail в тексте (https://gist.github.com/cgkio/7268045)
def extract_emails(text: str) -> list:
    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(pattern, text)
email_dict = {}

for item in data:
    inn = item.get('publisher_inn')
    text = item.get('msg_text', '')
    emails = extract_emails(text)

    if emails:
        if inn not in email_dict:
            email_dict[inn] = set()
        email_dict[inn].update(emails)

for inn, emails in email_dict.items():
    print(f'{inn}: {emails}')


# 3) Сохранение в JSON
with open('emails.json', 'w', encoding='utf-8') as f:
    json.dump({k: list(v) for k, v in email_dict.items()}, f, ensure_ascii=False, indent=2)

print('\nФайл emails.json сохранён.')
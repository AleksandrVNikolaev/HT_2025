import json
import csv
import re


def extract_emails(text: str) -> list:
    # Функция извлекает email-адреса из текста.
    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(pattern, text)


def main():
    # Задание "а" — загрузка ИНН из файла traders.txt
    with open(r'C:\Users\Lenovo\PycharmProjects\PythonProject\lesson_3\traders.txt', 'r') as file:
        inn_list = [line.strip() for line in file if line.strip()]

    print('Список ИНН из файла traders.txt:')
    for inn in inn_list:
        print(inn)

    # Задание "b_1" — загрузка организаций из traders.json
    with open(r'C:\Users\Lenovo\PycharmProjects\PythonProject\lesson_3\traders.json', 'r') as file:
        orgs = json.load(file)

    # Задание "b_2" — фильтрация организаций по ИНН
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

    # Задание "c" — запись в traders.csv
    with open('traders.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['short_name', 'inn', 'ogrn', 'address'], delimiter='|')
        writer.writeheader()
        writer.writerows(filtered_orgs)

    print('\nСохранено в файл traders.csv')

    # Задание 2. Сбор email-адресов из ЕФРСБ
    with open(r'C:\Users\Lenovo\PycharmProjects\PythonProject\lesson_3\1000_efrsb_messages.json', 'r') as file:
        data = json.load(file)

    email_dict = {}

    for item in data:
        inn = item.get('publisher_inn')
        text = item.get('msg_text', '')
        emails = extract_emails(text)

        if emails:
            if inn not in email_dict:
                email_dict[inn] = set()
            email_dict[inn].update(emails)

    # Печать найденных email-ов
    for inn, emails in email_dict.items():
        print(f'{inn}: {emails}')

    # Сохранение в файл emails.json
    with open('emails.json', 'w', encoding='utf-8') as f:
        json.dump({k: list(v) for k, v in email_dict.items()}, f, ensure_ascii=False, indent=2)

    print('\nФайл emails.json сохранён.')


if __name__ == '__main__':
    main()
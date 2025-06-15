import csv
import json
from decimal import Decimal
from time import time
from datetime import datetime, date, timedelta
import re
import os
from dadata import Dadata


DADATA_API_KEY = '1efd526145680ad2f94c2b7eb934a75bbf298a40'
DADATA_SECRET_KEY = '0e6d92377f6a71f5e8d382d7c37c06c576ee1622'
ddt = Dadata(DADATA_API_KEY, DADATA_SECRET_KEY)

a = ddt.find_by_id('party', '7701272485')
print(a)


BASE_DIR = os.path.dirname(__file__)
abs_path = os.path.join(BASE_DIR, r'C:\Users\Lenovo\PycharmProjects\PythonProject\1000_efrsb_messages.json')
efrsb_path = r'/1000_efrsb_messages.json'
# traders_csv_path = os.path.join(BASE_DIR, 'traders.csv)

start_time = time()
today = datetime.now()

due_term = 14
action_date = datetime(2025, 4, 8, 1, 1)

if action_date > (today - timedelta(days=due_term)):
    print('Срок не пропущен')
else:
    print('Срок пропущен')


print(today)

a = {'full_name': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ТОРГОВЫЙ ПАРТНЁР"',
     'short_name': 'ООО "ТОРГОВЫЙ ПАРТНЁР"',
     'inn': '6732101128',
     'ogrn': '1156733001424',
     'region': 'Смоленская область',
     'category': 'Обычная организация',
     'category_code': 'SimpleOrganization',
     'bankruptcy_id': '183678',
     'case_number': 'А62-10312/2017',
     'creation_date': today.isoformat(),
     'address': '214012, Смоленская обл, г Смоленск, ул Кашена, д 1, офис 719'
}

# with open('test.json', 'w') as f:
#     json.dump(a, f, ensure_ascii=False)


price_1 = Decimal('12.02')
price_2 = Decimal('11.01')
total = price_1 + price_2
print(total)




# with open(r'C:\Users\Lenovo\PycharmProjects\PythonProject\traders.txt', 'r') as file:
#     data_traders_txt = file.readlines()
#
#
# with open(efrsb_path, 'r') as file:
#     data_efrsb = json.load(file)
#
#
# with open(traders_csv_path, 'r') as file:
#     csv_file = csv.reader(file, delimiter='|')
#     for row in csv_file:
#         print(', '. join(row))
#     pass

end_time = time()
print(f'Выполнено за {end_time - start_time} сек')

def main():
    start_time = time()
    result = set()
    with open(r'/1000_efrsb_messages.json', 'r')as f:
        data = json.load(f)

        pattern = r'\b^\d{10}\b'
        for i in data:
            a = re.findall(pattern, i['msg_text'])
            if a:
                for y in a:
                    result.add(y)
        end_time = time()
        print('stop')


if __name__ == '__main__':
    main()
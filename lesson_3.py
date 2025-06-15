import csv
import json
from decimal import Decimal
from time import time
from datetime import datetime, date, timedelta
import re

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


abs_path = r'C:\Users\Lenovo\PycharmProjects\PythonProject\traders.txt'
efrsb_path = r'C:\Users\Lenovo\PycharmProjects\PythonProject\1000_efrsb_messages.json'
traders_csv_path = 'traders.csv'


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
    result = []
    with open(r'C:\Users\Lenovo\PycharmProjects\PythonProject\1000_efrsb_messages.json', 'r')as f:
        data = json.load(f)

        pattern = r'\b^\d{10}\b'
        for i in data:
            a = re.findall(pattern, i['msg_text'])
            pass

        print('stop')



if __name__ == '__main__':
    main()
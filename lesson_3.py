import csv
import json
from decimal import Decimal
from datetime import datetime


a = 0.123123

price_1 = Decimal('12.02')
price_2 = Decimal('11.01')
total = price_1 + price_2
print(total)


abs_path = r'C:\Users\Lenovo\PycharmProjects\PythonProject\traders.txt'
efrsb_path = r'C:\Users\Lenovo\PycharmProjects\PythonProject\1000_efrsb_messages.json'
traders_csv_path = 'traders.csv'


with open(r'C:\Users\Lenovo\PycharmProjects\PythonProject\traders.txt', 'r') as file:
    data_traders_txt = file.readlines()


with open(efrsb_path, 'r') as file:
    data_efrsb = json.load(file)


with open(traders_csv_path, 'r') as file:
    csv_file = csv.reader(file, delimiter='|')
    for row in csv_file:
        print(', '. join(row))
    pass

print('stop')
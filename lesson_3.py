import json

abs_path = r'C:\Users\Lenovo\PycharmProjects\PythonProject\traders.txt'
rel_path = r'C:\Users\Lenovo\PycharmProjects\PythonProject\1000_efrsb_messages.json'


with open(r'C:\Users\Lenovo\PycharmProjects\PythonProject\traders.txt', 'r') as file:
    data_2 = file.readlines()
    pass

with open(rel_path, 'r') as file:
    data_2 = json.load(file)
    pass

print('stop')
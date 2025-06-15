

abs_path = r'C:\Users\Lenovo\PycharmProjects\PythonProject\traders.txt'
rel_path = r'traders.txt'


file = open(rel_path, 'r')
data_1 = file.readlines()
file.close()

with open(r'C:\Users\Lenovo\PycharmProjects\PythonProject\traders.txt', 'r') as file:
    data_2 = file.readlines()

print('stop')
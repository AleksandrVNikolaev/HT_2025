from tkinter.font import names

a = 1 # int
print(id(a))
a = 1 + 2
print(id(a))
company_list = ['ООО "Рога и копыта"',
                'ООО "Креведка"',
                'ООО"Медвед"']

print(id(company_list))
company_list[0] = 'ЗАО "Рога и копыта"'
print(id(company_list))

b = 5.5 # float
c = True # bool
d = False

company_list = ['ООО "Рога и копыта"',
                'ООО "Креведка"',
                'ООО"Медвед"']

company_tuple = (company_list,
                'ООО "Креведка"',
                'ООО"Медвед"')

company_dict_1 = {'name':'ООО "Рога и копыта"',
                'address': 'Moscow, Arbat, 1',
                'inn': '8454365098',
                'employees': 16,
                'active': False}

company_dict_2 = {'name':'ООО "Рога и копыта"',
                'address': 'Moscow, Arbat, 1',
                'inn': '8454365098',
                'employees': 15,
                'active': False}

company_set = {'ООО "Рога и копыта"', 'ООО "Креведка"', 'ООО"Медвед"'}


statement_1 = True
statement_2 = False
print(statement_1 and statement_2)
print(statement_1 or statement_2)
print(not statement_1)
print(not statement_2)

bool()

if company_dict_2['employees'] % 2 == 0:
    print('Четное количество сотрудников')
else:
    print('Нечетное количество сотрудников')

try:
    company_dict_1['ogrn']
except KeyError:
    print('KeyError')
finally:
    print('finally')


if company_dict_1['inn'] == company_dict_2['inn']:
    print('Same company')
elif company_dict_1['inn'] != company_dict_2['inn']:
    print('Not same company')



# print(a+b+c)
#
# name = 'Kirill'
# surname = 'Sirotinsky'
#
# company = 'ООО "Рога и копыта"'
# print(name+' '+surname)
# print(company)
#
# company_list = ['ООО "Рога и копыта"',
#                 'ООО "Креведка"',
#                 'ООО"Медвед"']
#
# company_tuple = (company_list,
#                 'ООО "Креведка"',
#                 'ООО"Медвед"')
# print('before_change', company_list)
# company_list[0] = 'ЗАО "Рога и копыта"'
# print('after_change', company_list)
#
#
# name = 'Кружка'
# name = 'Стакан'
#
#
# company_list = [name, 'ООО "Креведка"', 'ООО"Медвед"']
#
# company_dict = {'name':'ООО "Рога и копыта"',
#                 'address': 'Moscow, Arbat, 1',
#                 'inn': '8454365098',
#                 'employers': 28,
#                 'active': True}
#
# company_dict['name'] = 'ПАО "Рога и копыта"'
# company_set = {'ООО "Рога и копыта"', 'ООО "Креведка"', 'ООО"Медвед"'}
# company_list[2] = 'ЗАО "Рога и копыта"'
# print(company_list)
#
# company = None
#
#
#
#
#
# print(company_dict)
# company_dict['name'] = 'ЗАО "Рога и копыта"'
# print(company_dict)
# company_dict['employers'] -= 5
# print(company_dict)
# company_dict['employers'] += 5
# print(company_dict)
#
# name = 'ООО "Креведка"'
# company_list = [name, 'ООО "Креведка"', 'ООО"Медвед"']
# company_list[0] = 'ЗАО "Рога и копыта"'
# print(company_list)
#
# # company_list = [company_dict, company_dict, company_dict]
# # print(company_list)
# # company_list[0]['name'] = 'ПАО "Рога и копыта"'
# # print(company_list)
#
#
#
#
#
# # print('before_change', company_list)
# # company_tuple[0] = 'ЗАО "Рога и копыта"'
# # print('after_change', company_list)
#
#
# print(company_list)
# print(company_list[-1])
# print(name[0])
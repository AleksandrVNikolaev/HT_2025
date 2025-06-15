# Домашнее задание № 3. Часть 1

# Задание 1. Факториал (●	функция вычисления факториала числа (произведение натуральных чисел от 1 до n).
# Принимает в качестве аргумента число, возвращает его факториал;)

def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
print(factorial(5))


# Задание 2. Наибольшее из трёх чисел (поиск наибольшего числа из трёх. Принимает в качестве аргумента кортеж
# из трёх чисел, возвращает наибольшее из них;)

def max_of_three(a, b, c):
    return max(a, b, c)
print(max_of_three(10, 20, 30))


# Задание 3. Площадь прямоугольного треугольника (●	расчёт площади прямоугольного треугольника.
# Принимает в качестве аргумента размер двух катетов треугольника. Возвращает площадь треугольника.)

def triangle_area(a, b):
    return (a * b) / 2
print(triangle_area(10, 20))


# Задание 4. Чётное или нечётное

def divide_with_no_remainder(n):
    return n % 2 == 0
print(divide_with_no_remainder(14))


# Домашнее задание № 3. Часть 2
# Генерация шапки процессуального документа по данным ответчика и суда

from lesson_2 import respondents, courts


def gen_header(respondent: dict) -> str:
    if 'case_number' not in respondent:
        return 'Ошибка: у ответчика отсутствует номер дела (case_number)'

    # Извлекаем номер дела из карточки ответчика
    case_number = respondent['case_number']

    # Получаем код суда — первые 3 символа номера дела
    court_code = case_number[:3]

    # Создаём словарь: код суда → карточка суда
    court_mapping = {court['court_code']: court for court in courts}

    # Ищем суд по коду
    court = court_mapping.get(court_code)

    # Если суд не найден — вернём сообщение об ошибке
    if not court:
        return f'Ошибка: код суда {court_code} не найден'

    # Формируем текст шапки
    header = (
        f'В {court["court_name"]}\n'
        f'Адрес: {court["court_address"]}\n\n'
        f'Истец: Николаев Александр Владиславович\n'
        f'ИНН 1234567890 \n'
        f'Адрес: 123100, г. Москва, 1-ый Красногвардейский проезд, 15\n\n'
        f'Ответчик: {respondent["short_name"]}\n'
        f'ИНН {respondent["inn"]} ОГРН {respondent["ogrn"]}\n'
        f'Адрес: {respondent["address"]}\n\n'
        f'Номер дела {case_number}'
    )

    return header

# Перебираем всех ответчиков и печатаем шапки
if __name__ == '__main__':
    for respondent in respondents:
        if 'case_number' in respondent:
            print(gen_header(respondent))
            print('\n' + '-' * 50 + '\n')

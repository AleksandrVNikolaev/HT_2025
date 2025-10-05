# Домашнее задание №11. Тема 3. Сетевое взаимодействие

import requests


class LegalAPI:
    """
    Класс для взаимодействия с Legal API (https://legal-api.sirotinsky.com/)

    Пример использования:
        api = LegalAPI(token="4123saedfasedfsadf4324234f223ddf23")
        debtor = api.get_debtor_info("7707083893")
        print(debtor)
    """

    BASE_URL = "https://legal-api.sirotinsky.com"

    def __init__(self, token: str):
        """
        Инициализация экземпляра класса.

        :param token: Токен авторизации (строка)
        """
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    # -------------------------------
    # Методы API
    # -------------------------------

    def get_debtor_info(self, inn: str) -> dict:
        """
        Получает сведения о должнике по ИНН из ЕФРСБ.

        :param inn: ИНН организации
        :return: словарь с данными о должнике
        """
        url = f"{self.BASE_URL}/efrsb/debtor/{inn}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_case_info(self, case_id: str) -> dict:
        """
        Получает сведения о конкретном деле по идентификатору.

        :param case_id: ID дела
        :return: словарь с информацией о деле
        """
        url = f"{self.BASE_URL}/cases/{case_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_publications(self, limit: int = 10) -> dict:
        """
        Получает последние публикации из ЕФРСБ.

        :param limit: количество публикаций
        :return: список публикаций в формате JSON
        """
        url = f"{self.BASE_URL}/publications?limit={limit}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_arbitral_managers(self, region: str = None) -> dict:
        """
        Получает список арбитражных управляющих.

        :param region: регион (опционально)
        :return: словарь с информацией о управляющих
        """
        url = f"{self.BASE_URL}/efrsb/managers"
        params = {"region": region} if region else {}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_companies(self, query: str) -> dict:
        """
        Выполняет поиск организаций по наименованию или ИНН.

        :param query: строка поиска (часть названия или ИНН)
        :return: список найденных компаний
        """
        url = f"{self.BASE_URL}/companies/search"
        params = {"query": query}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def check_connection(self) -> bool:
        """
        Проверяет доступность API.

        :return: True, если соединение установлено, иначе False
        """
        url = f"{self.BASE_URL}/ping"
        try:
            response = requests.get(url)
            return response.status_code == 200
        except requests.RequestException:
            return False


# Тестирование класса LegalAPI

from legal_api import LegalAPI


def main():
    token = "4123saedfasedfsadf4324234f223ddf23"
    api = LegalAPI(token)

    print("Проверка соединения с API:", api.check_connection())

    try:
        debtor = api.get_debtor_info("7707083893")
        print("Информация о должнике:")
        print(debtor)
    except Exception as e:
        print("Ошибка при получении данных о должнике:", e)

    try:
        publications = api.get_publications(limit=5)
        print("Последние публикации:")
        print(publications)
    except Exception as e:
        print("Ошибка при получении публикаций:", e)


if __name__ == "__main__":
    main()

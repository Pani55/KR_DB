from abc import ABC, abstractmethod
import requests


class Parser(ABC):
    """
    Абстрактный класс для парсинга данных.

    """
    @abstractmethod
    def load_vacancies(self, keyword):
        """
        Абстрактный метод для палучения данных с внешнего ресурса.

        :param keyword: Ключ-слово для фильтрации данных на внешнем ресурсе.
        """
        pass


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {'text': '', 'per_page': 100}
        self.vacancies = None

    def load_vacancies(self, keyword):
        """
        Метод для получения данных от API HeadHunter по ключ-слову от пользователя.

        :param keyword: Ключ-слово от пользователя.
        :return: response обЪект с ответом от API HEeadHunter.
        """
        self.params['text'] = keyword
        response = requests.get(self.url, params=self.params)
        self.vacancies = response.json()['items']

        return self.vacancies

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
        self.url = ''
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {}
        self.vacancies = []
        self.companies = []

    def load_vacancies(self, keyword: str = '', employer_id=''):
        """

        """
        self.url = 'https://api.hh.ru/vacancies'
        self.params['page'] = 0
        self.params['per_page'] = 100
        self.params['text'] = keyword
        if employer_id != '':
            self.params['employer_id'] = employer_id
        while self.params.get('page') != 10:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1

        return self.vacancies

    def load_companies(self, company_ids: list):

        for company_id in company_ids:
            self.url = 'https://api.hh.ru/employers/' + company_id
            response = requests.get(self.url, headers=self.headers, params=self.params)
            self.companies.append(response.json())

        return self.companies

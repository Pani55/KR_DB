class Vacancy:
    """
    Класс для работы с вакансиями: Создания экземпляров, валидации данных, полученных с API HeadHunter, и т.д.

    """

    def __init__(self, name: str, salary_from: int, salary_to: int, employer_id: str,
                 currency: str, requirements: str, url: str, city: str):
        self.name = name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.employer_id = employer_id
        self.currency = currency
        self.requirements = requirements
        self.url = url
        self.city = city

    def __repr__(self):
        return (f'{self.__class__.__name__}, {self.name}, {self.salary_from}, {self.salary_to},'
                f'{self.requirements}, {self.url}, {self.city}')

    @classmethod
    def cost_to_vacancies_obj_list(cls, hh_vacancies):
        """
        Классовый метод для создания экзэмпляров класса и укладки их в список.

        :param hh_vacancies: response обЪект - ответ от API HeadHunter.
        :return: Список экземпляров класса Vacancy.
        """
        vacancies_list = []
        for vacancy in hh_vacancies:
            name = vacancy['name']
            if not vacancy.get('salary'):
                salary_from = 0
                salary_to = 0
                currency = 0
            else:
                salary_from = Vacancy.validate_data_int(vacancy.get('salary').get('from'))
                salary_to = Vacancy.validate_data_int(vacancy.get('salary').get('to'))
                currency = vacancy['salary']['currency']
            employer_id = Vacancy.validate_data_str(vacancy['employer']['id'])
            requirements = vacancy['snippet']['requirement']
            url = vacancy['alternate_url']
            city = vacancy['area']['name']
            vacancy_object = cls(name, salary_from, salary_to, employer_id,
                                 currency, requirements, url, city)
            vacancies_list.append(vacancy_object)

        return vacancies_list

    def to_list(self):
        return [self.name, self.salary_from, self.salary_to, self.employer_id,
                self.currency, self.requirements, self.url, self.city]

    @staticmethod
    def validate_data_str(value):
        """
        Валидатор стороковых значений

        """
        if value:
            return value
        return 'информация не была найдена'

    @staticmethod
    def validate_data_int(value):
        """
        Валидатор интовых значений.

        """
        if value:
            return value
        return 0

    @staticmethod
    def print_vacancies(vacancies_list):
        """
        Статический метод для печати вакансий из списка в читабельном виде.

        :param vacancies_list: Список вакансий.
        """
        for vacancy in vacancies_list:
            print(vacancy)

    def __gt__(self, other):
        """
        Магический метод. Используется для сортировки списка по минимальной зарплате.

        """
        if not isinstance(other, (Vacancy, int)):
            raise TypeError('нит')
        if type(other) is type(self):
            return self.salary_from > other.salary_from
        return self.salary_from > other

    def __str__(self):
        return (f'============================================================'
                f'\nВакансия: {self.name}\n'
                f'Зарплата от {self.salary_from} до {self.salary_to} {self.currency}\n'
                f'Требования: {self.requirements}\n'
                f'Ссылка на страницу вакансии: {self.url}\n'
                f'Город: {self.city}\n'
                f'============================================================')
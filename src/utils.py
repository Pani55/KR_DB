from src.api_worker import HH
from src.vacancies import Vacancy
from src.companies import Company
from src.db_worker import DBManager


company_ids = ['81873', '1060821', '1122462', '2180', '87021',
               '1740', '1910225', '3844069', '15478', '78638']
hh_api = HH()


def user_interaction():
    """
    Функция для взаимодействия с пользователем.

    """
    print('Идёт создание таблиц в базе данных. Это может занять какое-то время.')
    for company_id in company_ids:
        hh_vacancies = hh_api.load_vacancies(employer_id=company_id)
    hh_companies = hh_api.load_companies(company_ids)
    vacancies_list = Vacancy.cost_to_vacancies_obj_list(hh_vacancies)
    companies_list = Company.cost_to_companies_obj_list(hh_companies)
    dbmanager = DBManager()
    dbmanager.create_comp_vacan_tables()

    while True:
        user_input = input('\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n'
                           'Перед вами локаничное меню для раьоты с приложением\n'
                           'Введите номер пункта меню для его выполнения:\n'
                           '1 - Загрузить информацию о вакансиях и компаниях на БД.\n'
                           '2 - Получить список всех компаний и количество вакансий у каждой компании.\n'
                           '3 - Получить список всех вакансий с указанием названия компании, '
                           'названия вакансии и зарплаты и ссылки на вакансию.\n'
                           '4 - Получить среднюю зарплату по вакансиям.\n'
                           '5 - Получить список всех вакансий, '
                           'у которых зарплата выше средней по всем вакансиям.\n'
                           '6 - Получить список всех вакансий, '
                           'в названии которых содержится переданное ключ-слово, например "python".\n'
                           'стоп/stop - Завершение работы.\n'
                           '|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n').lower()
        if user_input == '1':
            dbmanager.load_data_to_db(vacancies_list, companies_list)
            print('Таблицы были заполнены')
        elif user_input == '2':
            print(dbmanager.get_companies_and_vacancies_count())
        elif user_input == '3':
            print(dbmanager.get_all_vacancies())
        elif user_input == '4':
            print(dbmanager.get_avg_salary())
        elif user_input == '5':
            print(dbmanager.get_vacancies_with_higher_salary())
        elif user_input == '6':
            print(dbmanager.get_vacancies_with_keyword())
        elif user_input == 'stop' or user_input == 'стоп':
            exit()
        else:
            print('Такого пункта меню не существует. Попробуйте ещё раз.')

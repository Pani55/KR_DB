from src.api_worker import HH
from src.vacancies import Vacancy
from src.companies import Company
from src.db_worker import DBManager


"""company_ids = ['3127', '3776', '1122462', '2180', '87021',
               '1740', '80', '4181', '15478', '78638']
hh_api = HH()
hh_vacancies = []


for company_id in company_ids:
    hh_vacancies = hh_api.load_vacancies(employer_id=company_id)
hh_companies = hh_api.load_companies(company_ids)
vacancies_list = Vacancy.cost_to_vacancies_obj_list(hh_vacancies)
companies_list = Company.cost_to_companies_obj_list(hh_companies)
dbmanager = DBManager()
dbmanager.load_data_to_db(vacancies_list, companies_list)
print('Таблицы были заполнены')
"""

exe = DBManager()

print(exe.get_vacancies_with_keyword())
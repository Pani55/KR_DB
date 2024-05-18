import psycopg2


class DBManager:

    def __init__(self, dbname='KR_DB', user='postgres', password='Nik123666',
                 host='localhost', port='5432'):

        self.conn = psycopg2.connect(dbname=dbname, user=user,
                                     password=password, host=host,
                                     port=port)

        self.cur = self.conn.cursor()

        self.create_comp_vacan_tables()

    def create_comp_vacan_tables(self):
        """
        Метод для создания таблиц в базе данных

        """
        with self.conn:
            self.cur.execute(f""
                             f"CREATE TABLE IF NOT EXISTS employers ("
                             f"employer_id INT PRIMARY KEY,"
                             f"accredited VARCHAR,"
                             f"employer_name VARCHAR NOT NULL,"
                             f"description TEXT,"
                             f"url VARCHAR NOT NULL,"
                             f"vacancies_url VARCHAR NOT NULL,"
                             f"area VARCHAR"
                             f");")

        with self.conn:
            self.cur.execute(f""
                             f"CREATE TABLE IF NOT EXISTS vacancies ("
                             f"vacancy_id SERIAL PRIMARY KEY,"
                             f"vacancy_name VARCHAR NOT NULL,"
                             f"salary_from INT,"
                             f"salary_to INT,"
                             f"employer_id INT REFERENCES employers(employer_id) NOT NULL,"
                             f"currency VARCHAR,"
                             f"requirement TEXT,"
                             f"url VARCHAR NOT NULL,"
                             f"city VARCHAR"
                             f");")

    def load_data_to_db(self, vacancies, companies):
        """
        Метод для заполнения таблиц данными

        """
        for company in companies:
            with self.conn:
                self.cur.execute(f""
                                 f"INSERT INTO employers (employer_id,"
                                 f"accredited, employer_name, description, url,"
                                 f"vacancies_url, area) VALUES "
                                 f"(%s, %s, %s, %s, %s, %s, %s) returning *;", company.to_list())
        for vacancy in vacancies:
            try:
                with self.conn:
                    self.cur.execute(f""
                                     f"INSERT INTO vacancies (vacancy_name, salary_from, salary_to,"
                                     f"employer_id, currency, requirement, url, city) VALUES "
                                     f"(%s, %s, %s, %s, %s, %s, %s, %s) returning *;", vacancy.to_list())
            except psycopg2.errors.UniqueViolation:
                print(vacancy)

    def get_companies_and_vacancies_count(self):
        """
        метод для получения списка всех компаний кол-ва их вакансий

        """
        with self.conn:
            self.cur.execute(f""
                             f"SELECT employer_name, COUNT(vacancy_id)"
                             f"FROM employers "
                             f"JOIN vacancies USING(employer_id) "
                             f"GROUP BY employer_name;"
                             f"")
            return self.cur.fetchall()

    def get_all_vacancies(self):
        """
        Метод для получения списка всех вакансий

        """
        with self.conn:
            self.cur.execute(f""
                             f"SELECT vacancy_name, employer_name, salary_from, salary_to, vacancies.url "
                             f"FROM vacancies "
                             f"JOIN employers USING(employer_id)"
                             f"")
            return self.cur.fetchall()

    def get_avg_salary(self):
        """
        Метод для получения средней заработной платы по вакансиям

        """
        with self.conn:
            self.cur.execute(f""
                             f"SELECT AVG(salary_from + salary_to) AS avg_salary "
                             f"FROM vacancies"
                             f"")
            return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """
        Метод для получения списка вакансий с зп выше средней по всем вакансиям

        """
        with self.conn:
            self.cur.execute(f""
                             f"SELECT vacancy_name, city, salary_from, salary_to, vacancies.url "
                             f"FROM vacancies "
                             f"WHERE (salary_from + salary_to) / 2 > "
                             f"(SELECT AVG(salary_from + salary_to) AS avg_salary "
                             f"FROM vacancies)"
                             f"")
            return self.cur.fetchall()

    def get_vacancies_with_keyword(self):
        """
        Метод для получения списка вакансий по ключевому слову

        """
        user_input = input('Введите ключевое слово: ')

        with self.conn:
            self.cur.execute(f""
                             f"SELECT vacancy_name, employer_name, salary_from, salary_to, vacancies.url "
                             f"FROM vacancies "
                             f"JOIN employers USING(employer_id) "
                             f"WHERE vacancy_name LIKE '%{user_input}%'"
                             f"")
            return self.cur.fetchall()

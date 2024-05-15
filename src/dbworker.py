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
                                     f"currency, requirement, url, city) VALUES "
                                     f"(%s, %s, %s, %s, %s, %s, %s) returning *;", vacancy.to_list())
            except psycopg2.errors.UniqueViolation:
                print(vacancy)


DE = DBManager()
DE.create_comp_vacan_tables()

import psycopg2


# Подключение к базе данных
connection = psycopg2.connect(user="postgres",
                              password="Nik123666",
                              host="localhost",
                              port="5432",
                              database="HH_vacancies")

# Курсор для выполнения операций с базой данных
cursor = connection.cursor()

cursor.execute('CREATE TABLE ')
import psycopg2


def create_database(params, db_name) -> None:
    """
    Принимает параметры для подключения к БД и наименование БД.
    Создает новую БД.
    """

    connection = psycopg2.connect(database='postgres', **params)
    connection.autocommit = True
    cur = connection.cursor()
    try:
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")
    except psycopg2.ProgrammingError:
        pass

    cur.close()
    connection.close()


def create_table_employers(cur) -> None:
    """
    Принимает объект подключения к БД.
    Создает таблицу работодателей.
    """

    cur.execute('''
                CREATE TABLE employers
                (                
                employer_id_hh varchar(50) PRIMARY KEY NOT NULL,
                company_name varchar(100) NOT NULL,
                open_vacancies int,
                vacancies_url varchar(100) NOT NULL
                )
                ''')


def create_table_vacancies(cur) -> None:
    """
    Принимает объект подключения к БД.
    Создает таблицу вакансий.
    """

    cur.execute('''
                CREATE TABLE vacancies
                (                
                vacancy_id_hh varchar(50) PRIMARY KEY NOT NULL,
                vacancy_name varchar(150),
                employer_id_hh varchar(50) NOT NULL,
                vacancy_city varchar(50),
                min_salary int,
                max_salary int,
                vacancy_link varchar(50),
                FOREIGN KEY (employer_id_hh) REFERENCES employers(employer_id_hh)
                )
                ''')


def insert_table_employers(cur, list_data) -> None:
    """
    Принимает объект подключения к БД и список с данными о работодателях.
    Добавляет данные из списка в таблицу работодателей.
    """

    for row in list_data:
        add_table = tuple(row.values())
        cur.execute('INSERT INTO employers VALUES (%s, %s, %s, %s)', add_table)


def insert_table_vacancies(cur, list_data) -> None:
    """
    Принимает объект подключения к БД и список с данными о вакансиях.
    Добавляет данные из списка в таблицу вакансий.
    """

    for row in list_data:
        add_table = tuple(row.values())
        cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)', add_table)

import psycopg2

from config import config

from utils import get_employers, get_vacancies

from src.create_database import create_database, create_table_employers, create_table_vacancies, \
                            insert_table_employers, insert_table_vacancies

from DBManager import DBManager


def main():

    company_employers = get_employers()
    company_vacancies = get_vacancies(company_employers)

    db_name = 'database_coursework_5'

    params = config()
    conn = None

    create_database(params, db_name)
    print(f"\nБД {db_name} успешно создана\n")

    params.update({'dbname': db_name})

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:

                create_table_employers(cur)
                print("Таблица с работодателями успешно создана")

                create_table_vacancies(cur)
                print("Таблица с вакансиями успешно создана\n")

                insert_table_employers(cur, company_employers)
                print("Данные в таблицу работодателей успешно добавлены")

                insert_table_vacancies(cur, company_vacancies)
                print("Данные в таблицу вакансий успешно добавлены\n")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    db_manager = DBManager(params)
    db_manager.get_companies_and_vacancies_count()
    db_manager.get_all_vacancies()
    db_manager.get_avg_salary()
    db_manager.get_vacancies_with_higher_salary()
    db_manager.get_vacancies_with_keyword(input("Укажите слово для поиска вакансии в базе данных: "))


if __name__ == '__main__':
    main()

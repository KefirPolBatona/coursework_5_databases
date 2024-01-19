import psycopg2


class DBManager:
    """
    Класс для работы с данными в БД.
    """

    def __init__(self, params):
        """
        Принимает параметры для подключения к БД.
        Устанавливает соединение с БД.
        Инициализирует экземпляр класса.
        """

        self.params = params
        self.conn = psycopg2.connect(**self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """

        self.cur.execute('SELECT company_name, open_vacancies FROM employers')
        rows = self.cur.fetchall()
        for row in rows:
            print(f'У компании "{row[0]}" открытых вакансий: {row[1]}')
        print()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        self.cur.execute('''
                         SELECT company_name, vacancy_name, min_salary, vacancy_link
                         FROM employers
                         INNER JOIN vacancies USING(employer_id_hh)
                         ''')
        rows = self.cur.fetchall()
        for row in rows:
            print(f'Компания: "{row[0]}", вакансия: {row[1]}, зарплата: от {row[2]}, ссылка: {row[3]}')
        print()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям в БД.
        """

        self.cur.execute('''SELECT AVG(min_salary) FROM vacancies''')
        rows = self.cur.fetchone()
        print(f'Средняя зарплата в базе данных: {int(rows[0])}')
        print()
        return int(rows[0])

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """

        self.cur.execute(f'''
                         SELECT vacancy_name, min_salary 
                         FROM vacancies   
                         WHERE min_salary > {self.get_avg_salary()}                                                
                         ''')
        print('Вакансии с зарплатой выше среднего:')
        rows = self.cur.fetchall()
        for row in rows:
            print(f'{row[0]}, {row[1]}')
        print()

    def get_vacancies_with_keyword(self, user_input):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """

        self.cur.execute(f'''
                         SELECT vacancy_name 
                         FROM vacancies   
                         WHERE vacancy_name LIKE '%{user_input}%'                                                
                         ''')
        rows = self.cur.fetchall()
        if len(rows) > 0:
            print('Найдены вакансии:')
            for row in rows:
                print(f'{row[0]}')
        else:
            print('Вакансии не найдены')

        self.conn.commit()
        self.conn.close()

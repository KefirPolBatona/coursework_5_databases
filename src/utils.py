import json

import requests


def get_employers():
    """
    Осуществляет парсинг работодателей через API HH по заданным критериям и возвращает список словарей с ними.
    """

    company_employers = []
    req_employers = requests.get('https://api.hh.ru/employers', {'only_with_vacancies': True,
                                                                 'area': 113,
                                                                 'page': 0,
                                                                 'per_page': 10
                                                                 })
    data_employers = req_employers.content.decode()
    req_employers.close()
    dict_employers = json.loads(data_employers)

    for iteration in dict_employers['items']:
        company_employers.append({'employer_id_hh': iteration['id'],
                                  'employer_name': iteration['name'],
                                  'open_vacancies': iteration['open_vacancies'],
                                  'vacancies_url': iteration['vacancies_url']
                                  })

    return company_employers


def get_vacancies(company_employers):
    """
    Принимает список работодателей.
    Осуществляет парсинг вакансий у каждого работодателя через API НН и возвращает список словарей с ними.
    """

    company_vacancies = []

    for iteration in company_employers:
        req_company = requests.get(f'https://api.hh.ru/vacancies?employer_id={iteration["employer_id_hh"]}')
        data_company = req_company.content.decode()
        req_company.close()
        dict_company = json.loads(data_company)

        for iterat in dict_company['items']:
            company_vacancies.append({'vacancy_id_hh': iterat['id'],
                                      'vacancy_name': iterat['name'],
                                      'employer_id_hh': iterat['employer']['id'],
                                      'vacancy_city': iterat['area']['name'],
                                      'min_salary': iterat['salary']['from'],
                                      'max_salary': iterat['salary']['to'],
                                      'vacancy_link': iterat['alternate_url']
                                      })

    return company_vacancies

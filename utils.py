import psycopg2
import requests
from typing import Any
from googleapiclient.discovery import build
import time
import json

'''def get_vacancies(api_hh_ru: str, company_ids: list[str]) -> list[dict[str, Any]]:
    hh = build('hh', 'v3', developerKey=api_hh_ru)

    data = []
    for company_id in company_ids:
        company_data = hh.companies().list(part='snippet, statistics',id=company_id).execute()
        print(company_data)'''


def getEmployers():
    req = requests.get('https://api.hh.ru/employers')
    data = req.content.decode()
    req.close()
    count_of_employers = json.loads(data)['found']
    employers = []
    i = 0
    j = count_of_employers
    while i < j:
        req = requests.get('https://api.hh.ru/employers/' + str(i + 1))
        data = req.content.decode()
        req.close()
        jsObj = json.loads(data)
        try:
            employers.append([jsObj['id'], jsObj['name']])
            i += 1
            print([jsObj['id'], jsObj['name']])
        except:
            i += 1
            j += 1
        if i % 200 == 0:
            time.sleep(0.2)
    return employers


#employers = getEmployers()


def get_vacancies(employer_id):
    """Получение данных вакансий по API"""

    params = {
        'area': 1,
        'page': 0,
        'per_page': 10
    }
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    data_vacancies = requests.get(url, params=params).json()
    #print(data_vacancies)
    vacancies_data = []
    for item in data_vacancies["items"]:
        hh_vacancies = {
            'vacancy_id': int(item['id']),
            'vacancies_name': item['name'],
            'payment': item["salary"]["from"] if item["salary"] else None,
            'requirement': item['snippet']['requirement'],
            'vacancies_url': item['alternate_url'],
            'employer_id': employer_id
        }
        #if hh_vacancies['payment'] is not None:
        vacancies_data.append(hh_vacancies)

        #return vacancies_data
    print(vacancies_data)
#print(get_vacancies(205)))'''


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и их вакансиях

    :param database_name: (str) название базы данных
    :param params: (dict) параметры подключения к базе данных"""


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и их вакансиях

        :param database_name: (str) название базы данных
        :param params: (dict) параметры подключения к базе данных"""


def get_employer(employer_id):
    """Получаем данные о работодателях по API"""

    url = f"https://api.hh.ru/employers/{employer_id}"
    data_vacancies = requests.get(url).json()
    hh_company = {
        "employer_id": int(employer_id),
        "company_name": data_vacancies['name'],
        "open_vacancies": data_vacancies['open_vacancies']
    }
    #print(data_vacancies)
    #return hh_company
    print(hh_company)
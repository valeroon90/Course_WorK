import psycopg2
import requests
from typing import Any
from googleapiclient.discovery import build
import time
import json
from typing import List, Dict, Any


def get_hh_ru_data(company_ids: List[str]) -> List[Dict[str, Any]]:
    """
        Получение данных о работодателях и вакансиях с использованием API HH.ru.

        Параметры:
        - company_ids: Список строк, представляющих идентификаторы работодателей, для которых нужно получить данные.

        Возвращает:
        Список из словарей, (employers и vacancies) где каждый словарь содержит информацию о работодателе и список вакансий.
        """
    params = {
        'area': 1,
        'page': 0,
        'per_page': 10
    }
    data = []
    vacancies = []
    employers = []
    for employer_id in company_ids:
        url_emp = f"https://api.hh.ru/employers/{employer_id}"
        employer_info = requests.get(url_emp, params=params).json()
        employers.append(employer_info)


        url_vac = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
        vacancies_info = requests.get(url_vac, params=params).json()
        vacancies.append(vacancies_info)
    data.append({
        'employers': employers,
        'vacancies': vacancies
    })
    return data


def get_employer(company_ids):
    """Получаем краткие данные о наших работодателях по API"""
    data = []
    for employer_id in company_ids:
        url = f"https://api.hh.ru/employers/{employer_id}"
        data_vacancies = requests.get(url).json()

        hh_company = {
            "employer_id": int(employer_id),
            "company_name": data_vacancies['name'],
            "open_vacancies": data_vacancies['open_vacancies']
        }
        data.append(hh_company)
    return data


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




def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и их вакансиях

    :param database_name: (str) название базы данных, которую нужно создать
    :param params: (dict) параметры подключения к базе данных"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                company_name VARCHAR(300) NOT NULL,
                open_vacancies INTEGER,
                employer_url TEXT,
                description TEXT)
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                vacancy_name VARCHAR(300) NOT NULL,
                salary_from INTEGER,
                vacancy_url TEXT)
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях и их вакансиях """

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employers in data:
            employer_info = employers[employers]
            cur.execute(
                """
                INSERT INTO employers (company_name, open_vacancies, employer_url, description)
                VALUES (%s, %s, %s, %s)
                RETURNING employer_id
                """,
                (employer_info['name'], employer_info['open_vacancies'], employer_info['alternate_url'],
                 employer_info['description'])
            )
















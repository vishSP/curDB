import psycopg2
import requests

from classes import HH

hh = HH()


def companies():
    companies = []
    file = open('company.txt', encoding='utf-8')
    for i in file:
        companies.append(i.replace('\n', ""))
    file.close()
    return companies


def get_requests():
    url = 'https://api.hh.ru/employers'
    company = companies()
    all_companies = []
    for i in company:
        params = {'text': {i}, 'area': '113', 'only_with_vacancies': 'True'}
        data = requests.get(url, params=params).json()
        all_companies.append(data)
    return all_companies


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
                company_id serial PRIMARY KEY,
                company_name varchar (100) NOT NULL
            )
        """)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id serial PRIMARY KEY,
                vacancy_name varchar(100),
                salary int,
                url varchar(100),
                company_id int REFERENCES companies(company_id)
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data, database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            items = company.get('items')
            if not items:
                continue
            company_data = company['items'][0]

            cur.execute(
                """
                INSERT INTO companies (company_id,company_name)
                VALUES (%s, %s)
                RETURNING company_id
                """,
                (int(company_data['id']), company_data['name'])

            )

            company_id = cur.fetchone()[0]
            vacancies = hh.get_vacancies(company_id)

            for vacancy in vacancies:

                salary = vacancy['salary']

                if salary.get('from') is None:

                    salary = salary['to']
                else:
                    salary = salary['from']

                cur.execute(
                    """
            
                    INSERT INTO vacancies (vacancy_name, salary, url, company_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (vacancy['name'], salary, vacancy['url'],
                     company_id)
                )

    conn.commit()
    conn.close()

from configparser import ConfigParser

import psycopg2
import requests


def get_name_hh(data):
    """
    Ищет и возвращает имя вакансии

    """
    for i in data:
        i_data = i['items'][0]
        name = i_data['name']

    return name


def get_url_hh(data):
    """
    Ищет и возвращает ссылку вакансии

    """
    for i in data:
        i_data = i['items'][0]
        url = i_data['alternate_url']

    return url


def get_discription_hh(data):
    """
    Ищет и возвращает описание вакансии

    """
    for i in data:
        i_data = i['items'][0]
        discription = i_data['snippet']['responsibility']
        if i_data['snippet']['responsibility'] is None:
            return 'Нет описания'

    return discription


def get_salary_hh(data):
    """
    Ищет и возвращает зарпалату, либо ее отсутсвие

    """
    for i in data:
        i_data = i['items'][0]
        salary = i_data['salary']
        if salary['from'] is None:
            return salary['to']

        moder_salary = salary['from']
    return moder_salary


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


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
                company_id int PRIMARY KEY,
                company_name varchar (100) NOT NULL
            )
        """)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id int ,
                vacancy_name varchar(100),
                salary int,
                url varchar(100),
                company_id int REFERENCES companies(company_id)
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data, another_data, database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)
    print(another_data)
    with conn.cursor() as cur:
        for company in data:

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
            print(company_id)

            for vacancy in another_data:
                vacancy_data = vacancy['items'][0]
                salary = vacancy_data['salary']
                if salary.get('from') is None:

                    salary = salary['to']
                else:
                    salary = salary['from']

                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, vacancy_name, salary, url, company_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (vacancy_data['id'], vacancy_data['name'], salary, vacancy_data['url'],
                     company_id)
                )
    conn.commit()
    conn.close()

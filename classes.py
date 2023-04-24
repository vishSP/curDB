import requests
from utils import *
import psycopg2
from main import *


class HH:

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies/'

    def get_vacancies(self, company_id: int):
        params = {'employer_id': company_id, 'per_page': 100, 'only_with_salary': True}
        response = requests.get(url=self.__url, params=params).json()
        return response['items']

class DBManager:
    def __init__(self, params):
        conn = psycopg2.connect(dbname='postgres', **params)

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass
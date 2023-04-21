import requests
from utils import *
import psycopg2
from main import *


class HH:

    def __init__(self, data):
        self.data = data
        self.__url = 'https://api.hh.ru/vacancies/'
        self.__params = {'per_page': 100}

    def get_ids(self):
        company_data = self.data
        all_vacancies = []
        for company in company_data:

            another_data = company['items'][0]
            self.__params = {'employer_id': {another_data["id"]}, 'per_page': 100, 'only_with_salary': True}
            response = requests.get(url=self.__url, params=self.__params).json()
            all_vacancies.append(response)
        return all_vacancies


# class DBManager:
#
#     def get_DB(self):
#         with psycopg2.connect(host='localhost', database='hh', user='postgres', password='1620') as conn:
#             with conn.cursor() as cur:
#                 cur.execute("INSERT INTO companies VALUES (%s,%s)",
#                             (get_id(get_requests()), get_company_name(get_requests())))
#                 conn.commit()
#         conn.close()

# hh=HH(get_requests())
# print(hh.get_ids())
import requests
import psycopg2
from config import config


class HH:
    """
    Класс для работы с вакансиями НН
    """

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies/'

    def get_vacancies(self, company_id: int):
        """Получает вакансии"""
        params = {'employer_id': company_id, 'per_page': 100, 'only_with_salary': True}
        response = requests.get(url=self.__url, params=params).json()
        return response['items']


class DBManager:
    """
    Класс работает непосредственно с базой данной для вывода информации из нее
    """

    def __init__(self, params):
        self.params = config()
        self.conn = psycopg2.connect(dbname='hh_work', **params)

    def execute_query(self, query: str, fetch=False):
        """
        Функция создает курсор для передачи запроса
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            if fetch:
                return cur.fetchall()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        query = """
                SELECT company_name, COUNT(*) AS amount_vacancies
                FROM vacancies
                LEFT JOIN companies USING (company_id)
                GROUP BY company_name
                ORDER BY amount_vacancies DESC

        """
        rows = self.execute_query(query, fetch=True)
        return rows

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        query = """
                SELECT companies.company_name, vacancy_name, salary, url
                FROM vacancies
                JOIN companies USING (company_id)
                """
        rows = self.execute_query(query, fetch=True)
        return rows

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям.

        """
        query = """
                SELECT AVG(salary)
                FROM vacancies
        """
        rows = self.execute_query(query, fetch=True)
        return rows

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        query = """
                SELECT salary 
                FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                """
        rows = self.execute_query(query, fetch=True)
        return rows

    def get_vacancies_with_keyword(self, keyword: str):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
        """
        query = f"""
                SELECT company_name, v.* FROM companies
                JOIN vacancies v USING(company_id)
                WHERE LOWER(vacancy_name)
                LIKE LOWER('%{keyword}%')
                ORDER BY company_name
                """
        rows = self.execute_query(query, fetch=True)
        return rows

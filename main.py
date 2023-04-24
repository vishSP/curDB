import requests

from classes import DBManager
from utils import *
from classes import *


def main():
    params = config()

    data = get_requests()

    create_database('hh_work', params)
    save_data_to_database(data, 'hh_work', params)
    db = DBManager()
    db.get_companies_and_vacancies_count()


if __name__ == '__main__':
    main()

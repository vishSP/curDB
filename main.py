from classes import DBManager
from utils import *
from config import config


def main():
    """
    Основной цикл программы, отдает информацию в базу данных

    """
    params = config()

    data = get_requests()

    create_database('hh_work', params)
    save_data_to_database(data, 'hh_work', params)
    db = DBManager(params)


if __name__ == '__main__':
    main()

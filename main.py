import requests

from utils import *
from classes import *


def main():
    params = config()

    data = get_requests()
    hh = HH(get_requests())

    another_data = hh.get_ids()

    create_database('hh_work', params)
    save_data_to_database(data, another_data, 'hh_work', params)


if __name__ == '__main__':
    main()

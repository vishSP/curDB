Как работать с проектом
Установить PostgreSQL, если он не установлен.
Создать БД hh_work, для этого:
Запустить командную оболочку psql от пользователя с правами администратора
psql -U postgres
Ввести пароль
Создать БД head_hunter
CREATE DATABASE head_hunter;
Выйти из командной оболочки psql
exit
В конфигурационном файле db_config.ini (если нет файла - создать) проверить настройки подключения к БД. Если необходимо, указать актуальные настройки.
Для заполнения БД данными выполнить команду:
python main.py
Класс DBManager имеет следующие методы:
get_companies_and_vacancies_count(): возвращает список всех компаний и количество вакансий у каждой компании.
get_all_vacancies(): возвращает список всех вакансий с указанием названия компании, названия вакансии и зарплаты, ссылки на вакансию и города.
get_avg_salary(): возвращает среднюю зарплату по вакансиям.
get_vacancies_with_higher_salary(): возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
get_vacancies_with_keyword(): возвращает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
Для того чтобы воспользоваться этими методами:

импортируйте класс DBManager из модуля classes.py;

Пример:

from database import DBManager
from config import config

with DBManager(config()) as db:
  print(db.get_companies_and_vacancies_count())
  print(db.get_avg_salary())
  print(db.get_vacancies_with_keyword(keyword='Python'))
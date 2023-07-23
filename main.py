from classes import DBManager
from utils import create_database, save_data_to_database
from config import config


def main():
    params = config()
    create_database('hh_db', params)
    save_data_to_database('hh_db', params)

    hh_db = DBManager('hh_db', params)
    print(f"Список всех компаний и количество вакансий у каждой компании:"
          f" {hh_db.get_companies_and_vacancies_count()}")

    print(f"Список всех вакансий:"
          f" {hh_db.get_all_vacancies()}")

    print(f"Средняя зарплата по вакансиям:"
          f" {hh_db.get_avg_salary()}")

    print(f"Список всех вакансий, у которых зарплата выше средней:"
          f" {hh_db.get_vacancies_with_higher_salary()}")

    print(f"Список всех вакансий, в названии которых содержатся слова:"
          f" {hh_db.get_vacancies_with_keyword('python')}")


if __name__ == "__main__":
    main()

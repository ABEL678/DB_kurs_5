import psycopg2
from vacancies import get_vacancies


def create_database(database_name: str, params: dict):
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS employers (                            
                            employer_id INT PRIMARY KEY,
                            employer_name varchar(50) NOT NULL,
                            employer_url text                          
                            )                           
                        """)
    with conn.cursor() as cur:
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS vacancies (
                            vacancy_id INT PRIMARY KEY,
                            vacancy_name varchar(100) NOT NULL,
                            published_date date,
                            salary_from int,
                            salary_to int,
                            url text,
                            requirement text,
                            employer_id int REFERENCES employers (employer_id)
                            )
                        """)

    conn.commit()
    conn.close()


def save_data_to_database(database_name: str, params: dict):
    """Сохранение данных в базу данных."""
    data = get_vacancies()
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:

        for item in data:
            vacancy_id = item['id']
            vacancy_name = item['name']
            published_date = item['published_at']

            if item['salary'] is None:
                salary_from = '0'
                salary_to = '0'
            else:
                salary_from = item['salary']['from']
                salary_to = item['salary']['to']

            url = item['url']
            requirement = item['snippet']['requirement']
            employer_id = item['employer']['id']
            employer_name = item['employer']['name']
            employer_url = item['employer']['url']

            cur.execute("""                         
                         INSERT INTO employers VALUES (%s, %s, %s)
                         ON CONFLICT DO NOTHING
                        """,
                        (employer_id, employer_name, employer_url)
                        )

            cur.execute("""                          
                          INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)                          
                        """,
                        (vacancy_id, vacancy_name, published_date, salary_from, salary_to,
                         url, requirement, employer_id)
                        )

    conn.commit()
    conn.close()

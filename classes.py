import psycopg2


class DBManager:

    def __init__(self, database_name, params) -> None:
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=database_name, **params)

    def get_companies_and_vacancies_count(self):
        """Список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cur:
            cur.execute("""
                            SELECT DISTINCT employer_name FROM employers;
                            SELECT COUNT(*) FROM vacancies
                          """
                        )
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_all_vacancies(self):
        """Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cur:
            cur.execute("""
                            SELECT * FROM vacancies                            
                        """
                        )
            rows = cur.fetchall()
            for row in rows:
                print("Название вакансии:", row[1])
                print("Зарплата:", row[3])
                print("Ссылка на вакансию:", row[5])

    def get_avg_salary(self):
        """Средняя зарплата по вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""                            
                            SELECT AVG(salary_from - salary_to) FROM vacancies
                          """
                        )
            avg_salary = cur.fetchall()
            print(avg_salary)

    def get_vacancies_with_higher_salary(self):
        """Список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn.cursor() as cur:
            cur.execute("""
                            SELECT salary_to FROM vacancies
                        """
                        )
            rows = cur.fetchall()
            for row in rows:
                if row[3] >= self.get_avg_salary:
                    print("Название вакансии:", row[1])

    def get_vacancies_with_keyword(self, keyword='python'):
        """Список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”"""
        with self.conn.cursor() as cur:
            cur.execute("""
                            SELECT vacancy_name FROM vacancies                                                 
                        """
                        )
            rows = cur.fetchall()
            for row in rows:
                if keyword in row[1]:
                    print("Название вакансии:", row[1])
        cur.close()

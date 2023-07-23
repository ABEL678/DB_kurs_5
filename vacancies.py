import requests


url = "https://api.hh.ru/vacancies?employer_id="
headers = {
            "User-Agent": "MyImportantApp 1.0"
        }
params = {"pages": 100, "per_page": 50, "only_with_vacancies": True}
employers = [856498,  # Lesta_Games
             238161,  # Sigma
             42600,  # Naumen
             1993194,  # Yadro
             1009,  # CSBI
             61166,  # GIS
             8884,  # Dr.Web
             231166,  # ОЦРВ
             3778,  # Infotecs
             4801531  # Nedra_Digital
             ]


def get_vacancies():
    for employer_id in employers:
        response = requests.get(f"{url}{employer_id}", headers=headers, params=params)
        if response.status_code != 200:
            print(f"Ошибка {response.status_code}")
        else:
            return response.json()['items']

import requests
from tools import predict_rub_salary
import dotenv
import os


def predict_rub_salary(salary_from,salary_to):
    earn = 0
    if salary_from == None:
        earn = salary_to * 0.8
    elif salary_to == None:
        earn = salary_from * 1.2
    else:
        earn = (salary_from + salary_to) / 2
    return earn

def SuperJob_search(programming_languages):
    dotenv.load_dotenv()
    headers = {
            'X-Api-App-Id': os.getenv("APP_ID_SJ")
        }
    jobs_sj = {}
    for language in programming_languages:
        language_stats = {}
        vacancies_proseed = 0
        average_salaries = 0
        page = 0
        while True:
            params = {
            'town' : 'Moscow',
            'catalogues' : '48',
            'page': page,
            'keyword':language
            }
            response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers = headers,params=params)
            response.raise_for_status()
            for job in response.json()["objects"]:
                if job['currency'] == 'rub':
                    if job['payment_from'] !=0 or job['payment_to'] != 0:
                        vacancies_proseed += 1
                        salary = predict_rub_salary(job['payment_from'],job['payment_to'])
                        average_salaries += salary
            page += 1
            if response.json()['more'] == False:
                break
        try:
            average_salaries = int(average_salaries / vacancies_proseed)
        except ZeroDivisionError:
            average_salaries = 0
        language_stats['average_salary'] = average_salaries
        language_stats['found'] = response.json()['total']
        language_stats['proceed'] = vacancies_proseed
        jobs_sj[language] = language_stats
    return jobs_sj

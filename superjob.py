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

def superjob_search(programming_languages):
    dotenv.load_dotenv()
    headers = {
            'X-Api-App-Id': os.getenv("APP_ID_SJ")
        }
    jobs_sj = {}
    for language in programming_languages:
        language_stats = {}
        vacancies_processed = 0
        salaries_sum = 0
        catalogues = 48
        page = 0
        while True:
            params = {
            'town' : 'Moscow',
            'catalogues' : catalogues,
            'page': page,
            'keyword':language
            }
            response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers = headers,params=params)
            response.raise_for_status()
            vacancies = response.json()
            for job in vacancies["objects"]:
                if job['currency'] == 'rub':
                    if not job['payment_from']  or not job['payment_to']:
                        vacancies_processed += 1
                        salary = predict_rub_salary(job['payment_from'],job['payment_to'])
                        salaries_sum += salary
            page += 1
            if vacancies['more'] == False:
                break
        try:
            salaries_sum = int(salaries_sum / vacancies_processed)
        except ZeroDivisionError:
            salaries_sum = 0
        language_stats = {
            'found':vacancies['total'],
            'processed':vacancies_processed,
            'average_salary':salaries_sum
        }
        jobs_sj[language] = language_stats
    return jobs_sj

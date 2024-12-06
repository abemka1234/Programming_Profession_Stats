import requests
from itertools import count
from tools import predict_rub_salary

def headhunter_search(programming_languages):
    jobs_hh = {}
    for language in programming_languages:
        vacancies_processed = 0
        salaries_sum = 0
        language_stats = {}
        page = 0
        area = 1
        per_page = 100
        link = 'https://api.hh.ru/vacancies'
        for page in count(0,1):
            params = {'text':language,
                'area':area,
                'per_page':per_page,
                'page':page}
            response=requests.get(link, params = params)
            response.raise_for_status()
            vacancies = response.json()
            pages = vacancies['pages']
            if  page >= pages - 1:
                break
            for vacancy in vacancies['items']:
                if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR' and (vacancy['salary']['from']  or vacancy['salary']['to']):
                    vacancies_processed +=1
                    salaries_sum += predict_rub_salary(vacancy['salary']['from'],vacancy['salary']['to'])
        try:
            salaries_sum = int(salaries_sum / vacancies_processed)
        except ZeroDivisionError:
            salaries_sum = 0
        language_stats = {
            'found':vacancies['found'],
            'processed':vacancies_processed,
            'average_salary':salaries_sum
        }
        jobs_hh[language] = language_stats
    return jobs_hh
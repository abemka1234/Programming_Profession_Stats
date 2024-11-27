import requests
from tools import predict_rub_salary

def HeadHunter_search(programming_languages):
    jobs_hh = {}
    for language in programming_languages:
        vacancies_proseed = 0
        average_salaries = 0
        language_stats = {}
        page = 0
        link = 'https://api.hh.ru/vacancies'
        while True:
            params = {'text':language,
                'area':'1',
                'per_page':'100',
                'page':page}
            response=requests.get(link, params = params)
            response.raise_for_status()
            pages = response.json()['pages']
            if  page >= pages - 1:
                break
            page += 1
            for vacancy in response.json()['items']:
                if vacancy['salary'] and vacancy['salary']['currency'] == 'RUR':
                    vacancies_proseed +=1
                    average_salaries += predict_rub_salary(vacancy['salary']['from'],vacancy['salary']['to'])
        try:
            average_salaries = int(average_salaries / vacancies_proseed)
        except ZeroDivisionError:
            average_salaries = 0
        language_stats['found'] = response.json()['found']
        language_stats['proceed'] = vacancies_proseed
        language_stats['average_salary'] = average_salaries
        jobs_hh[language] = language_stats
    return jobs_hh
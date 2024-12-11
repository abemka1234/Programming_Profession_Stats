import requests
from tools import predict_rub_salary
from itertools import count


def superjob_search(programming_languages, app_id):
    headers = {"X-Api-App-Id": app_id}
    jobs_sj = {}
    for language in programming_languages:
        language_stats = {}
        vacancies_processed = 0
        salaries_sum = 0
        catalogues = 48
        page = 0
        for page in count(0, 1):
            params = {
                "town": "Moscow",
                "catalogues": catalogues,
                "page": page,
                "keyword": language,
            }
            response = requests.get(
                "https://api.superjob.ru/2.0/vacancies/", headers=headers, params=params
            )
            response.raise_for_status()
            vacancies = response.json()
            for job in vacancies["objects"]:
                if job["currency"] == "rub" and (
                    job["payment_from"] or job["payment_to"]
                ):
                    vacancies_processed += 1
                    salary = predict_rub_salary(job["payment_from"], job["payment_to"])
                    salaries_sum += salary
            if not vacancies["more"]:
                break
        try:
            salaries_sum = int(salaries_sum / vacancies_processed)
        except ZeroDivisionError:
            salaries_sum = 0
        language_stats = {
            "found": vacancies["total"],
            "processed": vacancies_processed,
            "average_salary": salaries_sum,
        }
        jobs_sj[language] = language_stats
    return jobs_sj


def predict_rub_salary(salary_from,salary_to):
    earn = 0
    if not salary_from:
        earn = salary_to * 0.8
    elif not salary_to:
        earn = salary_from * 1.2
    else:
        earn = (salary_from + salary_to) / 2
    return earn
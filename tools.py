
def predict_rub_salary(salary_from,salary_to):
    earn = 0
    if salary_from == None:
        earn = salary_to * 0.8
    elif salary_to == None:
        earn = salary_from * 1.2
    else:
        earn = (salary_from + salary_to) / 2
    return earn
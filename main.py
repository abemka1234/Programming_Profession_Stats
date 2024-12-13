import terminaltables
import headhunter
import superjob
import dotenv
import os

def make_table(languages,name):
    table_data = (('Язык','Вакансий найдено','Вакансий обработано','Средняя зарплата'),)
    for name_lang,lang_jobs in languages.items() :
        table_data +=((name_lang,lang_jobs['found'],lang_jobs['processed'],lang_jobs['average_salary']),)
    table = terminaltables.AsciiTable(table_data,name)
    return table.table


def main():
    dotenv.load_dotenv()
    programming_languages = ['JavaScript','Java','Python','Ruby','PHP','C++','CSS','C#','C','GO']
    jobs_hh = headhunter.headhunter_search(programming_languages)
    jobs_sj = superjob.superjob_search(programming_languages,os.getenv("APP_ID_SJ"))
    print(make_table(jobs_hh,'HeadHunter Професии'))
    print(make_table(jobs_sj,'Superjob Професии'))
    

if __name__ == "__main__":
    main()
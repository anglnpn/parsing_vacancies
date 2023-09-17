import json
import os
import requests

from classes import SuperJobAPI, HeadHunterAPI


def user_interaction():
    """
    Функция для работы с пользователем
    :return:
    """
    town = input("Введите город: ")
    search_query = input("Введите поисковый запрос: ")
    platform = input('Выберите платформу для поиска вакансий: "HeadHunter", "SuperJob" ')
    if platform == "HeadHunter":
        job_api = HeadHunterAPI(town, search_query)
        print(job_api.get_vacancies())
    elif platform == "SuperJob":
        job_api = SuperJobAPI(town, search_query)
        print(job_api.get_vacancies())

    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    # filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)

    # if not filtered_vacancies:
    #     print("Нет вакансий, соответствующих заданным критериям.")
    #     return

    # sorted_vacancies = sort_vacancies(filtered_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)


user_interaction()

# print(superjob_api)
# print(hh_api)
#
# job_api.get_vacancies()
# job_api.get_vacancies()

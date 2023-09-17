import json
import os
import requests
from abc import ABC, abstractmethod


class Job(ABC):
    """
    Абстрактный класс
    """

    @abstractmethod
    def get_vacancies(self):
        pass


class SuperJobAPI(Job):
    """
    Класс для получения вакансий с SuperJob
    """

    def __init__(self, town, search_query):
        """

        :param town: город пользователя
        :param search_query: поисковой запрос пользователя
        """
        self.town = town
        self.search_query = search_query

    def get_vacancies(self):
        """
        Метод для получения вакансий в формате JSON
        """
        sj_api_key: str = os.getenv('API_KEY_SJ')
        base_url = 'https://api.superjob.ru/2.0/'
        endpoint = 'vacancies'
        headers = {'X-Api-App-Id': sj_api_key}
        params = {
            'town': self.town,
            'keyword': self.search_query,
            # 'experience': 'no_experience',  # Опыт работы (no_experience, between1And3, moreThan6)
        }
        response = requests.get(f'{base_url}{endpoint}', headers=headers, params=params)

        vacancy_dict = {}
        vacancy_dict['people'] = []

        if response.status_code == 200:
            data = response.json()
            vacancies = data['objects']
            for prof in vacancies:
                payment_from = prof['payment_from']
                payment_to = prof['payment_to']
                profession = prof['profession']
                education = prof['education']['title']
                experience = prof['experience']['title']
                town = prof['town']['title']
                link = prof['link']

                dict_ = {"payment_from": payment_from, "payment_to": payment_to, "profession": profession,
                         "education": education, "experience": experience, "town": town, "link": link}

                vacancy_dict['people'].append(dict_)

            with open('super_job.json', 'w') as outfile:
                json.dump(vacancy_dict, outfile)

                # print(dict_)

                # if payment_to == 0:
                #     print(f"от {payment_from}")
                # else:
                #     print(f"от {payment_from} до {payment_to}")
                # print(education)
                # print(experience)
                # print(town)
                # print(f"{link}\n")

                # break
                # print(profession['profession'])

            # print(vacancies)
            # print(type(data))

        else:
            print('Ошибка при запросе данных:', response.status_code)


class HeadHunterAPI(ABC):
    """
        Класс для получения вакансий с HeadHunter
        """

    def __init__(self, town, search_query):
        """

         :param town: город пользователя
         :param search_query: поисковой запрос пользователя
         """
        self.areas_id = None
        self.town = town
        self.search_query = search_query

    def get_vacancies(self):
        """
            Метод для получения вакансий  по api
            в формате JSON
        """
        hh_api_key: str = os.getenv('API_KEY_HH')

        base_url = 'https://api.hh.ru/'
        endpoint = 'vacancies'

        if self.town:
            response = requests.get(f'{base_url}areas')
            areas_ = response.json()
            town_dict = {}
            for region in areas_[0]['areas']:
                for town_and_id in region["areas"]:
                    town_dict[town_and_id['name']] = town_and_id['id']

                for key, value in town_dict.items():
                    if key == self.town:
                        self.areas_id = value

        params = {'text': self.search_query, 'area': self.areas_id}

        # Выполнение запроса
        headers = {'Authorization': f'Bearer {hh_api_key}'}

        response = requests.get(f'{base_url}{endpoint}', params=params)

        if response.status_code == 200:
            data = response.json()
            vacancies = data['items']
            print(vacancies)
            # for prof in vacancies:
            #     payment_from = prof['salary']['to']
            #     payment_to = prof['payment_to']
            #     profession = prof['profession']
            #     education = prof['education']['title']
            #     experience = prof['experience']['title']
            #     town = prof['town']['title']
            #     link = prof['link']
            #
            #     print(profession)
            #     if payment_to == 0:
            #         print(f"от {payment_from}")
            #     else:
            #         print(f"от {payment_from} до {payment_to}")
            #     print(education)
            #     print(experience)
            #     print(town)
            #     print(f"{link}\n")
            # Здесь вы можете обработать список вакансий
        # else:
        # print('Ошибка при запросе данных:', response.status_code)

# """
# HEADHUNTER
# """
#
#
# hh_api_key: str = os.getenv('API_KEY_HH')
#
# head_hunter = build('youtube', 'v3', developerKey=hh_api_key)
#
# print(super_job)

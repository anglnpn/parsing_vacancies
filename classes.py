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

    @abstractmethod
    def sorted_vacancies(self):
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
        }
        response = requests.get(f'{base_url}{endpoint}', headers=headers, params=params)

        vacancy_dict = {'vacancy': []}

        if response.status_code == 200:
            data = response.json()
            vacancies = data['objects']
            for prof in vacancies:
                payment_from = prof['payment_from']
                payment_to = prof['payment_to']
                profession = prof['profession']
                experience = prof['experience']['title']
                town = prof['town']['title']
                url = prof['link']

                dict_vacancy = {"profession": profession, "town": town, "payment_from": payment_from,
                                "payment_to": payment_to, "experience": experience, "url": url}

                vacancy_dict['vacancy'].append(dict_vacancy)
            return vacancy_dict

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
        Метод для получения вакансий по api
        в формате JSON
        """

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

        response = requests.get(f'{base_url}{endpoint}', params=params)

        vacancy_dict = {'vacancy': []}

        if response.status_code == 200:
            data = response.json()
            vacancies = data['items']
            for prof in vacancies:

                url = prof['alternate_url']

                try:
                    payment_to = prof['salary']['to']
                    payment_from = prof['salary']['from']
                except TypeError:
                    payment_to = 0
                    payment_from = 0

                profession = prof['name']
                town = prof['area']['name']
                experience = prof['experience']['name']

                dict_vacancy = {"profession": profession, "town": town, "payment_from": payment_from,
                                "payment_to": payment_to, "experience": experience, "url": url}

                vacancy_dict['vacancy'].append(dict_vacancy)
            return vacancy_dict

        else:
            print('Ошибка при запросе данных:', response.status_code)


class FileManager(ABC):
    """
    Класс для работы с файлами
    """

    @abstractmethod
    def write(self, file):
        """
        Запись файла в json формат
        """
        pass

    @abstractmethod
    def read(self):
        """
        Чтение файла в json формате
        """
        pass


class JSONFileManager(FileManager):

    def __init__(self):
        self.file = None

    def write(self, file):
        """
        Запись файла в json формат
        """
        self.file = file
        with open('vacancy.json', 'w') as outfile:
            json.dump(self.file, outfile)

    def read(self):
        """
        Чтение файла в json формате
        """
        with open('vacancy.json', 'r', encoding='utf8') as outfile:
            read_file = json.load(outfile)
            print(read_file)

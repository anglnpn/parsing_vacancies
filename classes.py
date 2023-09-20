import json
import os
import requests
from abc import ABC, abstractmethod


class JobAPI(ABC):
    """
    Абстрактный класс для парсинга данных
    с платформ по API
    """

    @abstractmethod
    def parse_vacancies(self):
        """
        Получает вакансии по API и
        по введенным критериям(город, ключевое слово)

        :return: список json с вакансиями
        """
        pass

    @abstractmethod
    def formatting_vacancies(self, data):
        """
        Получает список json с вакансиями
        Форматирует вакансии и записывает данные в словарь
        для удобной работы.

        :param data:список json
        :return:отформатированный словарь
        """
        pass


class SuperJobAPI(JobAPI):
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
        self.vacancies = None

    def parse_vacancies(self):
        """
        Получает вакансии по API и
        по введенным критериям(город, ключевое слово)

        :return: список json с вакансиями
        """

        #
        sj_api_key: str = os.getenv('API_KEY_SJ')
        base_url = 'https://api.superjob.ru/2.0/'
        endpoint = 'vacancies'
        headers = {'X-Api-App-Id': sj_api_key}
        # определяем параметры запроса
        params = {
            'town': self.town,
            'keyword': self.search_query,
            'count': 100
        }
        # выполняем запрос
        response = requests.get(f'{base_url}{endpoint}', headers=headers, params=params)

        # возвращаем список вакансий в случае исполнения запроса без ошибок
        # если возникла ошибка выводим статус ошибки
        if response.status_code == 200:
            vacancies = response.json()
            return vacancies['objects']
        else:
            print('Ошибка при запросе данных:', response.status_code)

    def formatting_vacancies(self, data):
        """
          Получает список json с вакансиями
        Форматирует вакансии и записывает данные в словарь
        для удобной работы.

        :param data:список json
        :return:отформатированный словарь
        """
        self.vacancies = data

        formatted_vacancies_dict = {'vacancies': []}
        # записываем в цикле необходимые значения переменных
        for prof in self.vacancies:
            payment_from = prof['payment_from']
            payment_to = prof['payment_to']
            profession = prof['profession']
            experience = prof['experience']['title']
            town = prof['town']['title']
            url = prof['link']

            dict_vacancy = {"profession": profession,
                            "town": town,
                            "payment_from": payment_from,
                            "payment_to": payment_to,
                            "experience": experience,
                            "url": url}

            formatted_vacancies_dict['vacancies'].append(dict_vacancy)
        return formatted_vacancies_dict


class HeadHunterAPI(JobAPI):
    """
    Класс для получения вакансий с HeadHunter
    """

    def __init__(self, town, search_query):
        """

         :param town: город пользователя
         :param search_query: поисковой запрос пользователя
         """
        self.vacancies = None
        self.areas_id = None
        self.town = town
        self.search_query = search_query

    def parse_vacancies(self):
        """
        Получает вакансии по API и
        по введенным критериям(город, ключевое слово)

        :return: список json с вакансиями
        """

        base_url = 'https://api.hh.ru/'
        endpoint = 'vacancies'

        # находим индекс города по данным полученным по api с hh.ru
        # для определения индекса города и формирования запроса
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

        # определяем параметры запроса
        params = {'text': self.search_query,
                  'area': self.areas_id,
                  'per_page': 100}

        # выполняем запрос
        response = requests.get(f'{base_url}{endpoint}', params=params)

        if response.status_code == 200:
            vacancies = response.json()
            return vacancies['items']

        else:
            print('Ошибка при запросе данных:', response.status_code)

    def formatting_vacancies(self, data):
        """
          Получает список json с вакансиями
        Форматирует вакансии и записывает данные в словарь
        для удобной работы.

        :param data:список json
        :return:отформатированный словарь
        """
        self.vacancies = data

        formatted_vacancies_dict = {'vacancies': []}

        # форматируем вакансии
        for prof in self.vacancies:
            """
            payment_from инициализируется значением из prof['salary']['from'],
            если prof['salary'] существует и в нем есть ключ 'from'.
            В противном случае, payment_from устанавливается в None.
            Это означает, что если prof['salary']['from'] существует и не равно None,
            то payment_from примет значение из этого поля, иначе он будет None
            payment_to выполняет аналогичную операцию, но для поля 'to' в prof['salary'].
            """

            url = prof['alternate_url']
            payment_from = prof['salary']['from'] if prof['salary'] and 'from' in prof['salary'] else None
            payment_to = prof['salary']['to'] if prof['salary'] and 'to' in prof['salary'] else None

            if payment_from is None:
                payment_from = 0

            if payment_to is None:
                payment_to = 0

            profession = prof['name']
            town = prof['area']['name']
            experience = prof['experience']['name']

            dict_vacancy = {"profession": profession,
                            "town": town,
                            "payment_from": payment_from,
                            "payment_to": payment_to,
                            "experience": experience,
                            "url": url}

            formatted_vacancies_dict['vacancies'].append(dict_vacancy)
        return formatted_vacancies_dict


class FileManager(ABC):
    """
    Абстрактный класс для работы с файлами
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

    @abstractmethod
    def delete(self):
        """
        Удаляет информацию о вакансиях в json формате
        """
        pass


class JSONFileManager(FileManager):
    """
    Класс для записи и чтения файла в формате
    json.
    """

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
            return read_file

    def delete(self):
        """
        Удаляет информацию о вакансиях в json формате
        """
        with open('your_file.json', 'w') as file:
            json.dump({}, file)


class Vacancy:
    """
    Класс для сортировки вакансий
    """

    def __init__(self, file_vac):
        self.file_vac = file_vac["vacancies"]
        for element in self.file_vac:
            self.title = element["profession"]
            self.town = element["town"]
            self.payment_from = element["payment_from"]
            self.payment_to = element["payment_to"]
            self.experience = element["experience"]
            self.url = element["url"]

    def validate(self):
        """
        Проверка валидации данных
        :return: true or false
        """
        if not self.title or not self.payment_from or not self.payment_to:
            return False
        return True

    def sorted_salary_min(self):
        """
         Сортировка вакансий по возрастанию цены.
         Возвращает отсортированный список.
         """
        self.file_vac.sort(key=lambda x: x.get('payment_from', 0), reverse=False)

        return self.file_vac

    def sorted_salary_max(self):
        """
        Сортировка вакансий по убыванию цены.
        Возвращает отсортированный список.

        """
        self.file_vac.sort(key=lambda x: x.get('payment_from', 0), revers=True)
        return self.file_vac

    def sorted_vac_exp(self):
        pass

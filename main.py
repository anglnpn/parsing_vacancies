# Импорт классов
from classes import SuperJobAPI, HeadHunterAPI, JSONFileManager, Vacancy


def user_interaction():
    """
    Функция для работы с пользователем.
    Получает ввод данных
    Возвращает ответ в виде файла с вакансиями.
    Сортирует их по заданным критериям.

    """

    town = input("Введите город: ").title()
    search_query = input("Введите поисковый запрос: ").title()
    platform = input('Выберите платформу для поиска вакансий: "HeadHunter", "SuperJob"\n'
                     'Введите: "H" или "S"  \n').title()

    # Присваиваем переменной имя класса
    if platform == "H":
        platform_job = HeadHunterAPI
    else:
        platform_job = SuperJobAPI

    # создаем экземпляр класса
    job_api = platform_job(town, search_query)
    # вызываем метод для парсинга данных по api
    vacancies = job_api.parse_vacancies()
    # вызываем метод для форматирования вакансий по определенному шаблону
    vacancies_format = job_api.formatting_vacancies(vacancies)
    # создаем экземпляр класса для работы с файлом
    js_file = JSONFileManager()
    # вызываем метод форматирования
    js_file.write(vacancies_format)
    # читаем файл
    file_vac = js_file.read()
    print(file_vac)

    filter_vacancies = input("Включить фильтрацию вакансий по заработной плате?\n"
                             "Введите: 'да' или 'нет'  ")
    if filter_vacancies == 'да':
        # создаем экземпляр класса для работы с вакансиями
        vacancy_ = Vacancy(file_vac)
        range_amount = input("Сортировать по возрастанию или убыванию?\n"
                             "Введите; 'в' или 'у'  ")
        if range_amount == 'в':
            # вызываем метод для сортировки по убыванию
            print(vacancy_.sorted_salary_min())
        elif range_amount == 'у':
            # вызываем метод для сортировки по возрастанию
            print(vacancy_.sorted_salary_max())


if __name__ == "__main__":
    user_interaction()



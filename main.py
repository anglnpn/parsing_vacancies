# Импорт классов
from classes import SuperJobAPI, HeadHunterAPI, JSONFileManager, Vacancy


def user_interaction():
    """
    Функция для работы с пользователем.
    Получает ввод данных.
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
    elif platform == "S":
        platform_job = SuperJobAPI
    else:
        print("Введены некорректные данные. Завершение программы.")
        exit()

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

    # создаем экземпляр класса для работы с вакансиями
    vacancies_list = []
    for vac in file_vac['vacancies']:
        vacancy = Vacancy(vac)
        vacancies_list.append(vacancy)

    filter_vacancies = input("Включить фильтрацию вакансий по заработной плате?\n"
                             "Введите: 'да' или 'нет'  ")

    if filter_vacancies == 'да':

        range_amount = input("Сортировать по возрастанию или убыванию?\n"
                             "Введите; 'в' или 'у' ")
        count = 0
        if range_amount == 'у':
            # сортируем данные по возрастанию
            sorted_list = sorted(vacancies_list, reverse=True)
            for sort_vac in sorted_list:
                count += 1
                print(f'{count}) {sort_vac}')
        elif range_amount == 'в':
            # сортируем данные по убыванию
            sorted_list = sorted(vacancies_list, reverse=False)
            for sort_vac in sorted_list:
                count += 1
                print(f'{count}) {sort_vac}')
        else:
            print("Введены некорректные данные. Завершение программы.")
            exit()

        print(f"По вашему запросу выдано топ {count} вакансий по заработной плате")

    elif filter_vacancies == 'нет':
        print(vacancies_list)

    else:
        print("Введены некорректные данные. Завершение программы.")
        exit()


if __name__ == "__main__":
    user_interaction()




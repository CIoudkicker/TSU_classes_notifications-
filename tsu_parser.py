import requests
from typing import Any, Optional, List, Dict
import datetime
import json
from transliterate import translit
from datetime import datetime as dt

# JSON всех факультетов
URL_FACULTIES = "https://intime.tsu.ru/api/web/v1/faculties"

# JSON расписания для выбранной группы
URL_SCHEDULE = "https://intime.tsu.ru/api/web/v1/schedule/group"


# HTTP запрос к TSU API
class HttpRequest:
    # Отправка запроса
    def send_request(self, method: str, url: str, params=None) -> List[Dict[str, Any]]:
        response = requests.request(
            method=method,
            url=url,
            params=params
        )
        return self.__check_response(response)

    # Проверка запроса
    def __check_response(self, response: requests.Response) -> Optional[List[Dict[str, Any]]]:
        if response.status_code == 200:
            return response.json()
        else:
            error_message = f"Your request returned {response.status_code} status code."
            if response.status_code == 404:
                error_message += " The requested resource wasn't found."
            elif response.status_code == 500:
                error_message += " The server encountered an internal error."
            raise Exception(error_message)


# Получение даты для выполнения запроса к API и получения расписания группы
class Date:
    def __init__(self, date):
        if date is None:
            self.day = datetime.date.today()
        else:
            self.day = datetime.datetime.strptime(date, '%d.%m.%Y').date()

    def date_from(self) -> datetime.date:
        return self.day - datetime.timedelta(days=self.day.weekday())

    def date_to(self) -> datetime.date:
        return self.date_from() + datetime.timedelta(days=5)


# Обработка JSON файла после выполнения запроса
class ScheduleExtractor:
    def __init__(self, faculty, group_name, date=None):
        self.http_request = HttpRequest()
        self.date = date
        self.date_obj = Date(self.date)
        self.faculty = faculty
        self.group_name = group_name
        self.schedule_list = list()
        self.pure_schedule_list = dict()

    # Ссылка на список всех групп выбранного факультета
    def all_groups(self) -> str:
        faculty_id = self.get_faculty_id()
        url_group = f"{URL_FACULTIES}/{faculty_id}/groups"
        return url_group

    # Получение ID факультета для дальнейшего запроса к списку групп
    def get_faculty_id(self) -> Optional[str]:
        list_of_faculties = self.http_request.send_request("GET", URL_FACULTIES)
        for faculty in list_of_faculties:
            # Пример для этого факультета, нужно добавить входные данные
            if faculty.get("name") == self.faculty:
                return faculty.get("id")
        else:
            error = f"The {self.faculty} faculty wasn't found"
            raise Exception(error)

    # Запрос списка групп
    def get_groups_list(self) -> List[Dict[str, Any]]:
        url_group = self.all_groups()
        list_of_groups = self.http_request.send_request("GET", url_group)
        return list_of_groups

    # Поиск id группы по номеру
    def get_group_id(self) -> Optional[str]:
        groups_list = self.get_groups_list()
        for group in groups_list:
            if group.get("name") == self.group_name:
                return group.get("id")
        else:
            error = f"The {self.group_name} group wasn't found"
            raise Exception(error)

    # Запрос расписания для конкретной группы на сегодня
    def request_schedule(self) -> List[Dict[str, Any]]:
        params = {
            "id": self.get_group_id(),
            "dateFrom": self.date_obj.date_from(),
            "dateTo": self.date_obj.date_to()
        }
        self.schedule_list = self.http_request.send_request("GET", URL_SCHEDULE, params=params)
        self.form_pure_schedule_list()
        return self.schedule_list

    # Собрать все занятия по дням, по которым стоит отправлять уведомление
    def form_pure_schedule_list(self):
        self.schedule_list
        for day in self.schedule_list:
            self.pure_schedule_list[day.get("date")] = dict()
            for lessons in day.get("lessons"):
                if lessons.get("type") == "LESSON":

                    time = dt.fromtimestamp(lessons.get("starts")).time()
                    self.pure_schedule_list[day.get("date")][lessons.get("title")] = dict()
                    self.pure_schedule_list[day.get("date")][lessons.get("title")]["starts"] = dt.fromtimestamp(lessons.get("starts")).time()
                    self.pure_schedule_list[day.get("date")][lessons.get("title")]["ends"] = dt.fromtimestamp(lessons.get("ends")).time()
                    self.pure_schedule_list[day.get("date")][lessons.get("title")]["format"] = lessons.get("audience").get("name")

    # print расписания
    def print_schedule(self):
        print(self.schedule_list)

    # Сохранение в JSON
    def save_to_json(self):
        self.request_schedule()
        faculty_label_list = self.faculty.split()
        faculty_translited = translit("_".join(faculty_label_list), language_code="ru", reversed=True)
        pure_faculty_translited = "pure_" + faculty_translited
        with open(f"{faculty_translited}_{self.group_name}.json", "w") as file:
            json.dump(self.schedule_list, file, ensure_ascii=False)
        with open(f"{pure_faculty_translited}_{self.group_name}.json", "w") as file:
            json.dump(self.pure_schedule_list, file, ensure_ascii=False, default=str)


if __name__ == '__main__':
    current_faculty = "Институт прикладной математики и компьютерных наук"
    current_group = "932209"
    selected_day = "15.05.2023"
    schedule = ScheduleExtractor(current_faculty, current_group, selected_day)
    schedule.save_to_json()
    t = 0

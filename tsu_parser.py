import requests
from typing import Any, Optional
import datetime

# JSON всех факультетов
URL_FACULTIES = "https://intime.tsu.ru/api/web/v1/faculties"

# JSON расписания для выбранной группы
URL_SCHEDULE = "https://intime.tsu.ru/api/web/v1/schedule/group"


# HTTP запрос к TSU API
class HttpRequest:
    # Отправка запроса
    def send_request(self, method: str, url: str, params=None) -> list[dict[str, Any]]:
        response = requests.request(
            method=method,
            url=url,
            params=params
        )
        return self.__check_response(response)

    # Проверка запроса
    def __check_response(self, response: requests.Response) -> Optional[list[dict[str, Any]]]:
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
    def get_groups_list(self) -> list[dict[str, Any]]:
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
    def get_schedule(self) -> list[dict[str, Any]]:
        params = {
            "id": self.get_group_id(),
            "dateFrom": self.date_obj.date_from(),
            "dateTo": self.date_obj.date_to()
        }
        schedule_request = self.http_request.send_request("GET", URL_SCHEDULE, params=params)
        return schedule_request

    # print расписания
    def print_schedule(self):
        print(self.get_schedule())


if __name__ == '__main__':
    current_faculty = "Институт прикладной математики и компьютерных наук"
    current_group = "932209"
    selected_day = "01.05.2023"
    schedule = ScheduleExtractor(current_faculty, current_group, selected_day)
    schedule.print_schedule()

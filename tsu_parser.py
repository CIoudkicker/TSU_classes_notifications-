import requests
from typing import Any, Optional


# JSON всех факультетов
URL_FACULTIES = "https://intime.tsu.ru/api/web/v1/faculties"


# HTTP запрос к TSU API
class HttpRequest:
    # Отправка запроса
    def _request(self, method: str, url: str) -> list[dict[str, Any]]:
        response = requests.request(
            method=method,
            url=url
            # params=params
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


# Обработка JSON файла после выполнения запроса
# todo: Think about name of class
class JsonExtractor:
    def __init__(self):
        self.http_request = HttpRequest()

    # Ссылка на список всех групп выбранного факультета
    def group_url(self, faculty_id: str) -> str:
        url_group = f"{URL_FACULTIES}/{faculty_id}/groups"
        return url_group

    # Получение ID факультета для дальнейшего запроса к списку групп
    # todo: compare condition with the entered faculty name
    def get_faculty_id(self):
        list_of_faculties = self.http_request._request("GET", URL_FACULTIES)
        for faculty in list_of_faculties:
            # Пример для этого факультета, нужно добавить входные данные
            if faculty.get("name") == "Автономная образовательная программа TISP":
                faculty_id = faculty.get("id")
                print(faculty_id)


if __name__ == '__main__':
    x = JsonExtractor()
    x.get_faculty_id()

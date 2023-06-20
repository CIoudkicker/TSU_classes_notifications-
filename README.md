# Schedule Extractor

This is a Python script that extracts and saves the schedule data from the TSU API for a given faculty and group.

## Dependencies
- `requests`
- `typing`
- `datetime`
- `json`
- `transliterate`

You can install the dependencies by running the following command:
```
pip install requests typing datetime json transliterate
```

## Usage
1. Import the required modules: 

   ```python
    import requests
    from typing import Any, Optional, List, Dict
    import datetime
    import json
    from transliterate import translit
    from datetime import datetime as dt
    ```

2. Set the URLs for the TSU API endpoints:

    ```python
    URL_FACULTIES = "https://intime.tsu.ru/api/web/v1/faculties"
    URL_SCHEDULE = "https://intime.tsu.ru/api/web/v1/schedule/group"
    ```

3. Define the HttpRequest class for making HTTP requests to the TSU API:

    ```python
    class HttpRequest:
        # Sends an HTTP request and returns the response as JSON
        def send_request(self, method: str, url: str, params=None) -> List[Dict[str, Any]]:
            # ...
    
        # Checks the response status code and returns the JSON response if successful
        def __check_response(self, response: requests.Response) -> Optional[List[Dict[str, Any]]]:
            # ...
    ```

4. Define the `Date` class for obtaining the date range for the schedule request:

    ```python
    class Date:
        # Initializes the Date object with the current date or a provided date
        def __init__(self, date):
            # ...
    
        # Returns the start date for the schedule request (Monday of the week)
        def date_from(self) -> datetime.date:
            # ...
    
        # Returns the end date for the schedule request (Friday of the week)
        def date_to(self) -> datetime.date:
            # ...
    ```

5. Define the `ScheduleExtractor` class for extracting and processing the schedule data:

    ```python
    class ScheduleExtractor:
        # Initializes the ScheduleExtractor object with the given faculty, group, and date
        def __init__(self, faculty, group_name, date=None):
            # ...
    
        # Returns the URL for retrieving the list of all groups in the selected faculty
        def all_groups(self) -> str:
            # ...
    
        # Retrieves the ID of the selected faculty for further group list retrieval
        def get_faculty_id(self) -> Optional[str]:
            # ...
    
        # Sends a request to retrieve the list of groups in the selected faculty
        def get_groups_list(self) -> List[Dict[str, Any]]:
            # ...
    
        # Searches for the ID of the selected group in the list of groups
        def get_group_id(self) -> Optional[str]:
            # ...
    
        # Sends a request to retrieve the schedule for the selected group and date range
        def request_schedule(self) -> List[Dict[str, Any]]:
            # ...
    
        # Constructs a pure schedule list by filtering out non-lesson events
        def form_pure_schedule_list(self):
            # ...
    
        # Prints the raw schedule list
        def print_schedule(self):
            # ...
    
        # Saves the schedule to JSON files
        def save_to_json(self):
            # ...
    ```

6. In the ```if __name__ == '__main__':``` block, customize the input parameters:

    ```python
    if __name__ == '__main__':
        current_faculty = "Институт прикладной математики и компьютерных наук"
        current_group = "932209"
        selected_day = "15.05.2023"
        schedule = ScheduleExtractor(current_faculty, current_group, selected_day)
        schedule.save_to_json()
    ```
7. Run the script, and it will save the schedule data in JSON format.
 
> Note: Make sure to replace the `current_faculty`, `current_group`, and selected_day variables with your desired values.


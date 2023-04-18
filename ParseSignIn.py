from time import sleep
from time import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.common import exceptions as SeleniumExceptions
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
path = "https://moodle.tsu.ru/login/index.php"
driver.get(path)

def findXPathOnPage(function_to_decorate):
    def wrapper_findXPathOnPage(XPATH : str, text : str = None):
        startTimer = time() # точка отсчета времени
        while (True):
            try:
                element = driver.find_element(By.XPATH, XPATH)
                break
            except NoSuchElementException:
                findingTime = time() - startTimer  # время работы программы
                if findingTime > 10:
                    raise NoSuchElementException('Message: no such element: Unable to locate element: {"method":"xpath","selector":"'+XPATH+'"}')
                pass

        set_of_right_arguments = {"str", "int", "float"}

        if text is None:
            function_to_decorate(element)
        elif type(text).__name__ in set_of_right_arguments:
            function_to_decorate(element, str(text))
        else:
            raise SeleniumExceptions.InvalidArgumentException("Wrong argument type of text => (" + type(text).__name__ + " = " + str(text) + ") is passed")
    return wrapper_findXPathOnPage

# Функция которая нахожит кнопку "Войти через ТГУ аккаунт" при входе на сайт
@findXPathOnPage
def clickOn(clickElement):
    clickElement.click()

@findXPathOnPage
def setText(field, text):
    field.send_keys(text)


if __name__ == '__main__':

    email = "" # Введите сюда ваш логин/email
    password = "" # Введите сюда ваш пароль
    clickOn('//*[@id="login_url"]')
    setText('//*[@id="Email"]', email)
    setText('//*[@id="Password"]', password)
    clickOn('//*[@id="loginForm"]/form/div[3]/input[2]')

    sleep(100000)

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import time
from selenium.common import exceptions as SeleniumExceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

def findXPathOnPage(driver = None):
    def myDecorator(function_to_decorate):
        def wrapper_findXPathOnPage(self_Or_XPATH, XPATH : str = None, text : str = None):
            startTimer = time() # точка отсчета времени
            while (True):
                try:
                    if type(self_Or_XPATH).__name__ == "WebDriver":
                        element = self_Or_XPATH.find_element(By.XPATH, XPATH)
                    else:
                        element = self_Or_XPATH.driver.find_element(By.XPATH, XPATH)
                    break
                except NoSuchElementException:
                    findingTime = time() - startTimer  # время работы программы
                    if findingTime > 10:
                        raise NoSuchElementException('Message: no such element: Unable to locate element: {"method":"xpath","selector":"'+XPATH+'"}')
                    pass
                except AttributeError as attrError:
                    if str(attrError) == "'str' object has no attribute 'driver'":
                        t = 0
                        raise SeleniumExceptions.InvalidArgumentException(
                            "Wrong argument set is passed: you need to pass 'WebDriver' object as first argument")

            set_of_right_arguments = {"str", "int", "float"}

            if text is None:
                function_to_decorate(element)
            elif type(text).__name__ in set_of_right_arguments:
                function_to_decorate(element, str(text))
            else:
                raise SeleniumExceptions.InvalidArgumentException("Wrong argument type of text => (" + type(text).__name__ + " = " + str(text) + ") is passed")
        return wrapper_findXPathOnPage
    return myDecorator

class WorkWithSite:

    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.path = "https://moodle.tsu.ru/login/index.php"
        self.driver.get(self.path)

    # Функция которая нахожит кнопку "Войти через ТГУ аккаунт" при входе на сайт
    @findXPathOnPage()
    def clickOn(clickElement):
        clickElement.click()

    @findXPathOnPage()
    def setText(field, text):
        field.send_keys(text)

if __name__ == '__main__':
    signIn = WorkWithSite()
    signIn.clickOn('//*[@id="login_url"]')
    signIn.setText('//*[@id="Email"]', "") # Логин или email
    signIn.setText('//*[@id="Password"]', "") # Пароль
    signIn.clickOn('//*[@id="loginForm"]/form/div[3]/input[2]')

    sleep(100000)

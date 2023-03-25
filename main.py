from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
path = "https://intime.tsu.ru/"
driver.get(path)

# Функция нужна чтобы выяснить на сколько пикселей сдвинулся скролл в окне выбора
def findScrollingPixels(attributeValue : str):
    findStr = "transform: translateY("
    posTranslateY = attributeValue.find(findStr) + len(findStr)
    pxlsToScroll = ""
    while attributeValue[posTranslateY].isdigit():
        pxlsToScroll += attributeValue[posTranslateY]
        posTranslateY += 1
    return int(pxlsToScroll)

# Функция которая нахожит кнопку "Группы" при заходе на сайт
def clickOnGroupButton():
    groupButton = driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div[1]/div/div/button[1]')
    groupButton.click()

# Функция которая находит нужный факультет по имени, в противном случая возвращает False
def findFaculty(facultyName : str):

    nestedFaculties = driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div/div/div/div/div[1]')
    nestedFaculties.click()

    nestedList = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div[1]/div/div')
    scroll_origin = ScrollOrigin.from_element(nestedList)
    actions = ActionChains(driver)
    actions.move_to_element(nestedList)

    isFindFaculty = False
    memLastScrollPixels = 0
    actualScrollPixels = 1

    while isFindFaculty == False and memLastScrollPixels != actualScrollPixels:
        actions.scroll_from_origin(scroll_origin, 0, 100).perform()
        attributeValue = nestedList.get_attribute("style")
        memLastScrollPixels = actualScrollPixels
        actualScrollPixels = findScrollingPixels(attributeValue)
        try:
            faculty = driver.find_element(By.XPATH, '//*[@title="' + facultyName + '"]')
            faculty.click()
            isFindFaculty = True
            return faculty
        except NoSuchElementException:
            pass

    return isFindFaculty

# Функция которая находит нужную группу по номеру, в противном случая возвращает False
def findGroup(groupName : str):

    while(True):
        try:
            nestedGroup = driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div/div/div/div/div[2]/div')
            nestedGroup.click()
            break
        except NoSuchElementException:
            pass

    while(True):
        try:
            nestedList = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[1]')
            break
        except NoSuchElementException:
            pass

    scroll_origin = ScrollOrigin.from_element(nestedList)
    actions = ActionChains(driver)
    actions.move_to_element(nestedList)

    nestedList = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[1]/div/div')

    isFindGroup = False
    memLastScrollPixels = 0
    actualScrollPixels = 1

    while isFindGroup == False and memLastScrollPixels != actualScrollPixels:
        actions.scroll_from_origin(scroll_origin, 0, 100).perform()
        attributeValue = nestedList.get_attribute("style")
        memLastScrollPixels = actualScrollPixels
        actualScrollPixels = findScrollingPixels(attributeValue)
        try:
            group = driver.find_element(By.XPATH, '//*[@title="' + str(groupName) + '"]')
            group.click()
            isFindGroup = True
            return group
        except NoSuchElementException:
            pass

    return isFindGroup

# Когда факультет и группа выбраны появляется кнопка "Показать расписание" функция на нёё нажимает
def clickButtonShowShedule():
    while(True):
        try:
            ButtonShowShedule = driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div/div/div/div/button/span')
            ButtonShowShedule.click()
            break
        except NoSuchElementException:
            pass

if __name__ == '__main__':

    clickOnGroupButton()

    facultyName = "Институт прикладной математики и компьютерных наук"
    if findFaculty(facultyName):
        print("Finded faculty")
    else:
        print("Not finded faculty")

    groupName = 932201
    if findGroup(groupName):
        print("Group faculty")
    else:
        print("Not Group faculty")

    clickButtonShowShedule()

    sleep(100000)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

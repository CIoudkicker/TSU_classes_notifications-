from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    driver = webdriver.Chrome(executable_path=r'./chromedriver')
    ## open selenium URL in chrome browser
    ## /html/body/div/section/main/div/div[1]/div/div/button[1]
    path = "https://intime.tsu.ru/"
    driver.get(path)
    groupButton = driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div[1]/div/div/button[1]')
    groupButton.click()

    nestedFaculties = driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div/div/div/div/div[1]')
    nestedFaculties.click()

    # findMyFaculty = driver.find_element(By.XPATH, '//*[@title="Институт прикладной математики и компьютерных наук"]')
    # findMyFaculty.click()
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


    sleep(10000)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

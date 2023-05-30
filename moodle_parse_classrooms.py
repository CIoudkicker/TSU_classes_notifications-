import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from work_with_site import findXPathOnPage

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

    def scrape_links(self):
        element = self.driver.find_elements(By.XPATH, '//*[@id="inst1025821"]/div[2]/div[2]/table/tbody')

        links = { }

        for elem in element:
            title_element = elem.find_elements(By.CLASS_NAME, "b_title")
            for elemn in title_element:
                if elemn.text:
                    id = elemn.find_element(By.XPATH, "*").get_attribute("href").split("id=")[-1]
                    links[elemn.text] = "https://class.tsu.ru/m-course-" + id

        for key, value in links.items():
            print(key, value)

        with open('linksToClasses.json', 'w', encoding='utf-8') as f:
            json.dump(links, f, ensure_ascii=False, indent=4)

        return links


if __name__ == '__main__':
    signIn = WorkWithSite()
    signIn.clickOn('//*[@id="login_url"]')
    signIn.setText('//*[@id="Email"]', "ckontro@gmail.com")  # Логин или email
    signIn.setText('//*[@id="Password"]', "23347835Qq")  # Пароль
    signIn.clickOn('//*[@id="loginForm"]/form/div[3]/input[2]')

    time.sleep(30)

    signIn.scrape_links()
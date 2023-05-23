import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from lxml import html
from lxml import etree
from work_with_site import findXPathOnPage
from urllib.parse import urlparse, parse_qs
from io import StringIO


class ParseLinksFromSite:

    def get_links_from_table(xpath_expression):
        page = html.parse(StringIO('https://moodle.tsu.ru/my/'))
        elements = page.xpath('//*[@id="yui_3_17_2_1_1684808130405_393"]/tbody')[0].getchildren()
        links = []
        for element in elements:
            if 'class' in element.attrib and 'b_title' in element.attrib['class']:
                link = element.xpath('a')[0]
                links.append((link.attrib['href'], link.text))

        id_list = []
        for idlink, name in links:
            parsed_url = urlparse(idlink)
            query_params = parse_qs(parsed_url.query)
            id = query_params.get('id', [''])[0]
            id_list.append(id, name)

        audotoriesWithNames = []
        for classid, classname in id_list:
            url = "https://class.tsu.ru/m-course-{classid}"
            audotoriesWithNames.append([url, classname])

        # Тут по-хорошему передалать так, что бы не было разделения на 3 массива, но это потом
        # Когда пойму, что работает

        return audotoriesWithNames


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

        self.driver.implicitly_wait(70)

        element = self.driver.find_elements(By.XPATH, '//*[@id="inst1025821"]/div[2]/div[2]/table/tbody')

        # Получаем список элементов с классом "b_title"
        # links = element.find_elements(By.CLASS_NAME, "b_title")

        for elem in element:
            title_element = elem.find_elements(By.CLASS_NAME, "b_title")
            for elemn in title_element:
                print(elemn.text)


        # Создаем пустой словарь для хранения найденных ссылок
        links_dict = {}

        # Проходим по всем элементам с классом "b_title" и сохраняем их href
        # for link in links:
        #     href = link.get_attribute("href")
        #     name = link.text
        #     links_dict[name] = href

        # Возвращаем словарь с найденными ссылками

        # for link in links_dict:
        #     print(link[0], link[1])

        return links_dict


if __name__ == '__main__':
    signIn = WorkWithSite()
    signIn.clickOn('//*[@id="login_url"]')
    signIn.setText('//*[@id="Email"]', "ckontro@gmail.com")  # Логин или email
    signIn.setText('//*[@id="Password"]', "23347835Qq")  # Пароль
    signIn.clickOn('//*[@id="loginForm"]/form/div[3]/input[2]')

    time.sleep(60)

    signIn.scrape_links()

    # site = ParseLinksFromSite()
    # links = site.get_links_from_table()
    # for link in links:
    #     print(link[0], link[1])

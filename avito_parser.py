import json

from telebot import types
from keyboa import Keyboa

import undetected_chromedriver as us
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class AvitoParse:
    def __init__(self, url: list, items: list, count=100, version_main=None, limit = 0, userid = None):
        self.url = url
        self.items = items
        self.count = count
        self.version_main = version_main
        self.limit = limit
        self.userid = userid
        self.data = []

    def __set_up(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = us.Chrome(version_main=self.version_main, options=options)

    def __get_url(self):
        self.driver.get(self.url)

    def __paginator(self):
        while self.driver.find_elements(By.CSS_SELECTOR, "[data-marker*='pagination-button/next']") and self.count > 0:
            self.__parse_page()
            self.driver.find_element(By.CSS_SELECTOR, "[data-marker*='pagination-button/next']").click()
            self.count -= 1

    def __parse_page(self):
        titles = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        for title in titles:
            name = title.find_element(By.CSS_SELECTOR, "[itemprop='name']").text
            description = title.find_element(By.CSS_SELECTOR, "[class*='item-description']").text
            url = title.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute("href")
            price = title.find_element(By.CSS_SELECTOR, "[itemprop='price']").get_attribute("content")
            data = {
                'name': name,
                'description': description,
                'url': url,
                'price': price
            }
            if any([item.lower() in description.lower() for item in self.items]) and int(price) == 0:
                self.data.append(data)
                print(data)
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("Товар на авито", url=url))
                mes_text = "*Наименование:*\n{}\n\n*Цена:*\n{}\n\n*Описание*\n{}".format(name, price, description)
                bot.send_message(self.userid, mes_text, reply_markup=markup, parse_mode="Markdown")


                self.__save_data()

    def __save_data(self):
        with open("items.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def parse(self):
        self.__set_up()
        self.__get_url()
        self.__paginator()

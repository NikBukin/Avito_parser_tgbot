import telebot
from telebot import types
import time
import pandas as pd
from keyboa import Keyboa

import avito_parser
import config
import users_par

bot = telebot.TeleBot(config.token, skip_pending=True)

user_dict = {}


class User:
    def __init__(self, userid):
        self.userid = userid

        self.userfirstname = None
        self.userlastname = None

        self.start_quest = None

        self.param_city = None
        self.param_interval = None
        self.param_item = None
        self.param_price = None


# Создание списка с id пользователей для проверки наличия доступа

users = list(pd.read_csv('users_card.csv', delimiter=',')['userid'])


# команда /start
@bot.message_handler(commands=['start']
    , func=lambda message: message.chat.id in users
                     )
def send_start(message):
    user_card_p = pd.read_csv('users_card.csv', delimiter=',')
    if message.chat.id in list(user_card_p['userid']):
        chat_id = message.chat.id
        userid = message.chat.id
        user = User(userid)
        user_dict[chat_id] = user
        user.userfirstname = message.chat.first_name
        user.userlastname = message.chat.last_name

        text_list = ["💸 Халява", "💰 Поиск по цене", "🎛️ Изменить параметры"]

        complete_keyboa = Keyboa(items=text_list, copy_text_to_callback=True)

        bot.send_message(message.chat.id, text="Добро пожаловать в тестовый бот по поиску дешевых товаров на "
                                                     "*Aвито*!\nЗдесь вы можете выбрать два алгоритма работы "
                                                     "бота:\n\n* - ПОИСК ХАЛЯВЫ*\n_предназначен для поиска "
                                                     "бесплатных товаров по заданным параметрам_\n\n* - ПОИСК ПО "
                                                     "ЗАДАННОЙ ЦЕНЕ*\n_Предназначен для поиска товаров по заданной цене_",
                               reply_markup=complete_keyboa(), parse_mode="Markdown")
        bot.send_message(message.chat.id,
                         text="Перед началом использования алгоритма необходимо задать базовые параметры",
                         parse_mode="Markdown")


@bot.message_handler(content_types=['Начать заново'])
def send_welcome(message):
    user_card_p = pd.read_csv('users_card.csv', delimiter=',')
    if message.chat.id in list(user_card_p['userid']):
        chat_id = message.chat.id
        userid = message.chat.id
        user = User(userid)
        user_dict[chat_id] = user
        user.userfirstname = message.chat.first_name
        user.userlastname = message.chat.last_name

        text_list = ["💸 Халява", "💰 Поиск по цене", "🎛️ Изменить параметры"]

        complete_keyboa = Keyboa(items=text_list, copy_text_to_callback=True)


        msg = bot.send_message(message.chat.id, text="Выберите алгоритм работы бота:"
                                                     "\n\n* - ПОИСК ХАЛЯВЫ*\n_предназначен для поиска "
                                                     "бесплатных товаров по заданным параметрам_\n\n* - ПОИСК ПО "
                                                     "ЗАДАННОЙ ЦЕНЕ*\n_Предназначен для поиска товаров по заданной цене_",
                               reply_markup=complete_keyboa(), parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def start_bot(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.stat_quest = message.text
    if message.text == "Халява":
        free_item_def(message)
    elif message.text == "Поиск по цене":
        find_by_price_def(message),
    elif message.text == "Изменить параметры":
        change_param_city_def(message)

    if not (message.text == "Халява" or message.text == "Поиск по цене" or message.text == "Изменить параметры"
            or message.text == "/start" or message.text == "Начать заново"):
        msg = bot.send_message(message.chat.id, 'Я вас не понимаю... Пожалуйста, выберите из предложенных вариантов')
        bot.register_next_step_handler(msg, start_bot)


def free_item_def(message):
    pass


def find_by_price_def(message):
    pass


def change_param_city_def(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in config.goroda:
        markup.add(types.KeyboardButton(i))

    msg = bot.send_message(message.chat.id,
                           text="Пожалуйста, укажите город, в котором необходимо осуществлять поиск товаров",
                           reply_markup=markup, parse_mode="Markdown")

    bot.register_next_step_handler(msg, change_param_interval_def)


def change_param_interval_def(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.param_city = message.text
    if message.text == "/start":
        send_welcome(message)
    elif message.text in config.goroda:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in config.time_interval:
            markup.add(types.KeyboardButton(i))

        msg = bot.send_message(message.chat.id, text="Укажите с каким интервалом необходимо осуществлять поиск товара",
                               reply_markup=markup, parse_mode="Markdown")

        bot.register_next_step_handler(msg, change_param_item_def)
    if not (message.text in config.goroda or message.text == "/start" or message.text == "Начать заново"):
        msg = bot.send_message(message.chat.id, 'Я вас не понимаю... Пожалуйста, выберите из предложенных вариантов')
        bot.register_next_step_handler(msg, start_bot)


def change_param_item_def(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.param_interval = message.text
    if message.text == "/start":
        send_welcome(message)
    elif message.text in config.time_interval:
        markup = types.ReplyKeyboardRemove()

        msg = bot.send_message(message.chat.id, text="Какой товар необходимо искать?"
                                                     "\n\n_Напишите наименование с клавиатуры_",
                               reply_markup=markup, parse_mode="Markdown")

        bot.register_next_step_handler(msg, change_param_price_def)


def change_param_price_def(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.param_item = message.text
    markup = types.ReplyKeyboardRemove()

    msg = bot.send_message(message.chat.id, text="Введите предельную цену товара (числом с клавиатуры)"
                                                 "\n\n_Будет использоваться при выборе алгоритма «Поиск по цене»_",
                           reply_markup=markup, parse_mode="Markdown")

    bot.register_next_step_handler(msg, change_param_final_def)


def change_param_final_def(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.param_price = message.text
    if message.text == "/start":
        send_welcome(message)
    elif message.text.isdigit():
        print(user.param_interval)
        print(user.param_price)
        print(user.param_item)
        print(user.param_city)
        markup = types.ReplyKeyboardRemove()

        msg = bot.send_message(message.chat.id, text="Отлично, мы сохранили Ваши параметры."
                                                     "\n Таким образом:",
                               reply_markup=markup, parse_mode="Markdown")
        text_params = "🛒 Товар - {}\n" \
                      "💰 Предельная цена - {}\n" \
                      "🏙 Город - {}\n" \
                      "⏱ Интервал - {}\n".format(user.param_item, user.param_price, user.param_city,
                                                 user.param_interval)
        users_par.save_param(user.userid, user.userfirstname, user.userlastname, user.param_city, user.param_interval,
                             user.param_price, user.param_item)
        bot.send_message(message.chat.id, text=text_params, parse_mode="Markdown")

        send_welcome(message)


@bot.callback_query_handler(func=lambda message: True)
def callback_inline(call):
    chat_id = call.from_user.id
    user = user_dict[chat_id]
    print(call.data)
    if call.data == '🎛️ Изменить параметры':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in config.goroda:
            markup.add(types.KeyboardButton(i))

        msg = bot.send_message(chat_id,
                               text="Пожалуйста, укажите город, в котором необходимо осуществлять поиск товаров",
                               reply_markup=markup, parse_mode="Markdown")

        bot.register_next_step_handler(msg, change_param_interval_def)

    if call.data == '💸 Халява':
        avito_parser.AvitoParse(url="https://www.avito.ru/all/bytovaya_elektronika?cd=1&q=%D0%BE%D1%82%D0%B4%D0%B0%D0%BC+%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE",
                                count = 1,
                                version_main=116,
                                items=["iphone","телевизор"]
                                ).parse()
        print("поиск закончен")
        pass

    if call.data == '💰 Поиск по цене':
        pass











# if __name__ == '__main__':
#     while True:
#         try:
#             bot.polling(none_stop=True, skip_pending=True)
#         except Exception as e:
#             time.sleep(3)
#             print(e)


bot.polling(none_stop=True, skip_pending=True)

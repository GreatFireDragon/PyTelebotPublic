import telebot
from telebot import types
import bs4_functions
from random import randrange

import opencv as ocv
import commands
import thiscodedoesnotexist as dne



API_KEY = '5263831940:AAGxk7T_bP7eQGDmKeH6sopuVCH7dpY_8bo'
bot = telebot.TeleBot(API_KEY)  # Создаем экземпляр бота



operation = ""          # Для обработки фото
# -----------------------------------------------------------------------
# Функция, которая отпарвляет "пока не работает"
def not_available_yet(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, text="Пока не работает")

# Функция, которая отпарвляет "Пришлите фото для обработки"
def send_photo_please(message):
    global operation            # Для обработки фото делаем глобальной
    chat_id = message.chat.id
    bot.send_message(chat_id, text="Пришлите фото для обработки")
    operation = message.text

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(commands.dict["main_menu"])
    btn2 = types.KeyboardButton(commands.dict["help"])
    markup.add(btn1, btn2)

    bot.send_message(chat_id, text="Привет, {0.first_name}! ".format(message.from_user), reply_markup=markup)

# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == commands.dict["main_menu"]:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(commands.dict["fun"])
        btn2 = types.KeyboardButton(commands.dict["web-cam"])
        btn3 = types.KeyboardButton(commands.dict["valute"])
        btn4 = types.KeyboardButton(commands.dict["images"])
        btn5 = types.KeyboardButton(commands.dict["news"])
        btn6 = types.KeyboardButton(commands.dict["settings"])
        back = types.KeyboardButton(commands.dict["help"])
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, back)

        bot.send_message(chat_id, text="Вы в главном меню", reply_markup=markup)

# -----------------------------------------------------------------------
    elif ms_text == "Выбрать другой способ обработки":
        ocv.main_func(message.chat.id)

# Развлечения -----------------------------------------------------------
    elif ms_text == commands.dict["fun"]:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(commands.dict["cat"])
        btn2 = types.KeyboardButton(commands.dict["human"])
        btn3 = types.KeyboardButton(commands.dict["joke"])
        back = types.KeyboardButton(commands.dict["main_menu"])
        markup.add(btn1, btn2, btn3, back)

        bot.send_message(chat_id, text="Доступные развлечения:", reply_markup=markup)

# Развлечения дальше:  ---------------------------------
    elif ms_text == commands.dict["cat"]:
        dne.send_cat(message)

    elif ms_text == commands.dict["human"]:
        dne.send_person(message)

    elif ms_text == commands.dict["joke"]:
        hahaha = bs4_functions.get_anekdot()
        bot.send_message(chat_id, hahaha)

# -----------------------------------------------------------------------
    elif ms_text == commands.dict["news"]:
        news = bs4_functions.get_news(message)
        bot.send_message(chat_id, news)

# Главное меню --------------------------------
    elif ms_text == commands.dict["web-cam"]:
        not_available_yet(message)

    elif ms_text == commands.dict["settings"]:
        not_available_yet(message)

    elif ms_text == commands.dict["valute"]:
        ans = bs4_functions.valute()
        bot.send_message(chat_id, text=ans)

# Обработка изображений --------------------------------
    elif ms_text == commands.dict["images"]:
        ocv.main_func(chat_id)

    elif ms_text == commands.dict["canny"] or ms_text == commands.dict["ch_b"] \
            or ms_text == commands.dict["blur"] or ms_text == commands.dict["mirror"] \
            or ms_text == commands.dict["mirror2"] or ms_text == commands.dict["cartoon"]:
        send_photo_please(message)


# -----------------------------------------------------------------------

    elif ms_text == commands.dict["help"]:

        chat_id = message.chat.id
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Написать автору", url="https://t.me/GreatFireDragon")
        markup.add(btn1)
        try:
            bot.send_photo(chat_id, 'https://static.independent.co.uk/2021/06/16/08/newFile-4.jpg?quality=75&width=982&height=726&auto=webp',
                       caption="Автор: Кулешов МС 1МД25", reply_markup=markup)
        except Exception:
            bot.send_photo(chat_id,
                           open('images/tea.jpg', "rb"),
                           caption="Автор: Кулешов МС 1МД25", reply_markup=markup)


# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
    else:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton(commands.dict["main_menu"])
        markup.add(back)

        pone_seed = str(randrange(10000, 99999))
        pone_seed = 'https://thisponydoesnotexist.net/v1/w2x-redo/jpgs/seed' + pone_seed + '.jpg'


        bot.send_photo(chat_id,
                       pone_seed,
                       caption="Я не знаю такой комманды. \nПотерялся? Попробуй написать /start", reply_markup=markup)


# -----------------------------------------------------------------------
@bot.message_handler(commands=["help"])
def start(message, res=False):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(commands.dict["main_menu"])
    btn2 = types.KeyboardButton(commands.dict["help"])
    markup.add(btn1, btn2)

    bot.send_message(chat_id, text="Привет, {0.first_name}! ".format(message.from_user), reply_markup=markup)

# -----------------------------------------------------------------------
# Обработка изображений
@bot.message_handler(content_types=['photo'])
def photo(message):

    chat_id = message.chat.id
    global operation

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("input_image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    if operation == commands.dict["blur"]:

        stringList = (10, 20)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for value in stringList:
            btn = types.KeyboardButton(str(value))
            markup.add(btn)

        msg = bot.reply_to(message, "Выберите степень блюра (Или напишите своё целое число)", reply_markup=markup)
        bot.register_next_step_handler(msg, ocv.blur_matrix_step)

    elif operation == commands.dict["ch_b"]:
        ocv.chb("input_image.jpg")
        ocv.all_done_photo(chat_id)

    elif operation == commands.dict["canny"]:

        stringList = (50, 100, 200)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for value in stringList:
            btn = types.KeyboardButton(str(value))
            markup.add(btn)

        msg = bot.reply_to(message, "Выберите параметр выделения краёв (Или напишите своё целое число)", reply_markup=markup)
        bot.register_next_step_handler(msg, ocv.canny_matrix_step)

    elif operation == commands.dict["mirror"]:
        ocv.mirror_y("input_image.jpg")
        ocv.all_done_photo(chat_id)

    elif operation == commands.dict["mirror2"]:
        ocv.mirror_x("input_image.jpg")
        ocv.all_done_photo(chat_id)

    elif operation == commands.dict["cartoon"]:

        stringList = (8, 16, 24)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for value in stringList:
            btn = types.KeyboardButton(str(value))
            markup.add(btn)

        msg = bot.reply_to(message, "Выберите количество цветов (Или напишите своё целое число)",
                           reply_markup=markup)
        bot.register_next_step_handler(msg, ocv.cartoon_matrix_step)

    else:
        ocv.main_func(message.chat.id)
        return



# -----------------------------------------------------------------------

bot.polling(none_stop=True, interval=0) # Запускаем бота
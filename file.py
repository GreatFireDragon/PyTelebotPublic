import json
from io import BytesIO

import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types
import requests
import bs4
import botGames  # бот-игры, файл botGames.py

import menuBot
from menuBot import Menu, Users  # в этом модуле есть код, создающий экземпляры классов описывающих моё меню
import DZ  # домашнее задание от первого урока

import commands as cm
import thiscodedoesnotexist as dne
import bs4_functions
import opencv as ocv
from random import randrange



bot = telebot.TeleBot('5263831940:AAGxk7T_bP7eQGDmKeH6sopuVCH7dpY_8bo')  # Создаем экземпляр бота
game21 = None  # класс игры в 21, экземпляр создаём только при начале игры
rsp = None
operation = "" # Для обработки фото, хранит знаечние выполняемой операции



def my_input(bot, chat_id, txt, proc_answer):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, proc_answer)

# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands=['start', 'help'])
def start_command(message, res=False):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAIf6GJep0_9zQfeIs2l0sngNhSi3SCDAAK-AAPcZzkodjBnwrqp_owkBA')
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, cm.dict["main_menu"]).markup)


@bot.message_handler(commands=["cur_menu"])
def cur_menu_command(message, res=False):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAIhcmJjAyK5xPEtNi6cy--4BqDBaV7JAALdEgACyeBBStA1_gy3V6EIJAQ')
    try:
        ans = Menu.cur_menu.get(chat_id).name
    except Exception:
        ans = "\nОШИБКА\nВозвращаю в главное меню."

    txt_message = f"Я нахожусь тут: {ans}"
    bot.send_message(chat_id, text=txt_message)

# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
# Получение стикеров от юзера
@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

    # глубокая инспекция объекта
    # import inspect,pprint
    # i = inspect.getmembers(sticker)
    # pprint.pprint(i)


# -----------------------------------------------------------------------
# Получение аудио от юзера
@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)


# -----------------------------------------------------------------------
# Получение голосовухи от юзера
@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    bot.send_message(message.chat.id, voice)


# -----------------------------------------------------------------------
# Получение фото от юзера
@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)


# -----------------------------------------------------------------------
# Получение видео от юзера
@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)


# -----------------------------------------------------------------------
# Получение документов от юзера
@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")


# -----------------------------------------------------------------------
# Получение координат от юзера
@bot.message_handler(content_types=['location'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    location = message.location
    bot.send_message(message.chat.id, location)

    # from Weather import WeatherFromPyOWN
    # pyOWN = WeatherFromPyOWN()
    # bot.send_message(chat_id, pyOWN.getWeatherAtCoords(location.latitude, location.longitude))
    # bot.send_message(chat_id, pyOWN.getWeatherForecastAtCoords(location.latitude, location.longitude))


# -----------------------------------------------------------------------
# Получение контактов от юзера
@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)



# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = Users.getUser(chat_id)
    if cur_user == None:
        cur_user = Users(chat_id, message.json["from"])

    # проверка = мы нажали кнопку подменю, или кнопку действия
    subMenu = menuBot.goto_menu(bot, chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if subMenu != None:
        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if subMenu.name == cm.dict["21"]:
            game21 = botGames.newGame(chat_id, botGames.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif subMenu.name == cm.dict["rsp"]:
            gameRSP = botGames.newGame(chat_id, botGames.RSP_game())  # создаём новый экземпляр игры и регистрируем его
            text_game = "<b>Победитель определяется по следующим правилам:</b>\n" \
                        "1. Камень побеждает ножницы\n" \
                        "2. Бумага побеждает камень\n" \
                        "3. Ножницы побеждают бумагу\n" \
                        "подробная информация об игре: <a href='https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D0%BC%D0%B5%D0%BD%D1%8C,_%D0%BD%D0%BE%D0%B6%D0%BD%D0%B8%D1%86%D1%8B,_%D0%B1%D1%83%D0%BC%D0%B0%D0%B3%D0%B0'>Wikipedia</a>"
            bot.send_photo(chat_id, photo="https://i.ytimg.com/vi/Gvks8_WLiw0/maxresdefault.jpg", caption=text_game, parse_mode='HTML')

        elif subMenu.name == cm.dict["wordle"]:
            wordle = botGames.newGame(chat_id, botGames.Wordle('CRANE'))  # создаём новый экземпляр игры и регистрируем его
            text_game = f"Это игра <b>wordle</b>. У вас будет {wordle.guess_number} попыток угадать <b>пятизначное</b> слово.\n<b>Зелёная</b> буква стоит на <b>своей</b> позиции\n" \
                        f"<b>Жёлтая</b> буква <b>есть</b> в слове, но стоит <b>не на своём</b> месте\n<b>Чёрной</b> буквы <b>нет</b> в слове"
            bot.send_photo(chat_id, photo="https://www.aljazeera.com/wp-content/uploads/2022/01/INTERACTIVE-How-to-play-wordle_1.png", caption=text_game, parse_mode='HTML')
            print("chat_id = " + str(chat_id) + ", wordle answer: " + str(wordle.answer))

        elif subMenu.name == cm.dict["wordle_m"]:
            print("Hello, I can hear you!")


        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu != None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню

        if ms_text == cm.dict["help"]:
            send_help(chat_id)

        elif ms_text == cm.dict["cat"]:
            dne.send_cat(message)

        elif ms_text == cm.dict["human"]:
            dne.send_person(message)

        elif ms_text == cm.dict["pony"]:
            dne.send_pony(chat_id)

        elif ms_text == cm.dict["joke"]:
            bot.send_message(chat_id, text=get_anekdot())

        elif ms_text == cm.dict["movie"]:
            send_film(chat_id)

# bot.send_photo(chat_id, game21.arr_cards_URL[-1], caption=text_game)
# -----------------------------------------------------------------------
    #Игра 21
        elif ms_text == cm.dict["card"]:

            game21 = botGames.getGame(chat_id)
            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                menuBot.goto_menu(bot, chat_id, cm.dict["exit"])
                return

            text_game = game21.get_cards(1)
            bot.send_photo(chat_id, game21.arr_cards_URL[-1], caption=text_game)
            # bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            # bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена
                botGames.stopGame(chat_id)
                menuBot.goto_menu(bot, chat_id, cm.dict["exit"])
                return

        elif ms_text == cm.dict["stop"]:
            botGames.stopGame(chat_id)
            menuBot.goto_menu(bot, chat_id, cm.dict["exit"])
            return
# -----------------------------------------------------------------------
# Игра Rock Scissors Paper
        elif ms_text in (cm.dict["rock"], cm.dict["paper"], cm.dict["scissors"]):
            rsp = botGames.RSP_game()
            ans = rsp.get_rules(ms_text)
            bot.send_message(chat_id, text="Я выбрал " + ans[0] + "...")
            bot.send_message(chat_id, text="Получается, " + ans[1])

# -----------------------------------------------------------------------
        elif ms_text == cm.dict["full_pattern"]:
            wordle = botGames.getGame(chat_id)
            bot.send_message(chat_id, wordle.full_pattern())
            return


# -----------------------------------------------------------------------
# Игра RSP Multiplayer
        elif ms_text == cm.dict["rsp_m"]:
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text="Создать новую игру", callback_data="GameRPSm|newGame")
            keyboard.add(btn)
            numGame = 0
            for game in botGames.activeGames.values():
                if type(game) == botGames.GameRPS_Multiplayer:
                    numGame += 1
                    btn = types.InlineKeyboardButton(
                        text= str(numGame) + " игроков: " + str(len(game.players)),
                        callback_data="GameRPSm|Join|" + menuBot.Menu.setExtPar(game))
                    keyboard.add(btn)
            btn = types.InlineKeyboardButton(text="Вернуться", callback_data="GameRPSm|Exit")
            keyboard.add(btn)

            bot.send_message(chat_id, text=botGames.GameRPS_Multiplayer.name, reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(chat_id, "Вы хотите начать новую игру, или присоединиться к существующей?",
                             reply_markup=keyboard)

# -----------------------------------------------------------------------
# Игра Wordle Multiplayer
        elif ms_text == cm.dict["wordle_m"]:
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text="Создать новую игру", callback_data="Wordle_m|newGame")
            keyboard.add(btn)
            numGame = 0
            for game in botGames.activeGames.values():
                if type(game) == botGames.Wordle_Multiplayer:
                    numGame += 1
                    btn = types.InlineKeyboardButton(
                        text= str(numGame) + " игроков: " + str(len(game.players)),
                        callback_data="Wordle_m|Join|" + menuBot.Menu.setExtPar(game))
                    keyboard.add(btn)
            btn = types.InlineKeyboardButton(text="Вернуться", callback_data="Wordle_m|Exit")
            keyboard.add(btn)

            bot.send_message(chat_id, text=botGames.Wordle_Multiplayer.name, reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(chat_id, "Вы хотите начать новую игру, или присоединиться к существующей?",
                             reply_markup=keyboard)

        # -----------------------------------------------------------------------
        elif ms_text == cm.dict["№1"]:
            DZ.dz1(bot, chat_id)

        elif ms_text == cm.dict["№2"]:
            DZ.dz2(bot, chat_id)

        elif ms_text == cm.dict["№3"]:
            DZ.dz3(bot, chat_id)

        elif ms_text == cm.dict["№4"]:
            DZ.dz4(bot, chat_id)

        elif ms_text == cm.dict["№5"]:
            DZ.dz5(bot, chat_id)

        elif ms_text == cm.dict["№6"]:
            DZ.dz6(bot, chat_id)

        elif ms_text == cm.dict["№7"]:
            DZ.dz7(bot, chat_id)
# -----------------------------------------------------------------------
# Новости и статистика --------------------------------
        elif ms_text == cm.dict["news"]:
            news = bs4_functions.get_news(message)
            bot.send_message(chat_id, news)

        elif ms_text == cm.dict["valute"]:
            ans = bs4_functions.valute()
            bot.send_message(chat_id, text=ans)

# -----------------------------------------------------------------------
# Обработка изображений --------------------------------
        elif ms_text == cm.dict["canny"] or ms_text == cm.dict["ch_b"] \
                or ms_text == cm.dict["blur"] or ms_text == cm.dict["mirror"] \
                or ms_text == cm.dict["mirror2"] or ms_text == cm.dict["cartoon"]:
            send_photo_please(message)

    else:  # ........................................................................................
        if cur_menu != None and cur_menu.name == cm.dict["wordle"]:
            wordle = botGames.getGame(chat_id)

            if ms_text == cm.dict["exit"]:
                menuBot.goto_menu(bot, chat_id, cm.dict["exit"])
                return

            ans = wordle.check_guess(ms_text)
            bot.send_message(chat_id, ans)

            if wordle.end_of_game == True:  # выход, если игра закончена
                botGames.stopGame(chat_id)
                menuBot.goto_menu(bot, chat_id, cm.dict["exit"])
                return

        elif cur_menu != None and cur_menu.name == cm.dict["wordle_m"]:
            bot.send_message(chat_id, "Ты зашёл в wordle multiplayer")
            bot.send_message(chat_id, "Пока разрабатывается")

        else:
            bot.send_message(chat_id, "Я не знаю такой команды")
            menuBot.goto_menu(bot, chat_id, cm.dict["main_menu"])
# -----------------------------------------------------------------------



# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать параметр или несколько параметров в обработчик кнопки,
    # используйте методы Menu.getExtPar() и Menu.setExtPar()
    # call.data это callback_data, которую мы указали при объявлении InLine-кнопки
    # После обработки каждого запроса вызовете метод answer_callback_query(), чтобы Telegram понял, что запрос обработан
    chat_id = call.message.chat.id
    message_id = call.message.id
    cur_user = Users.getUser(chat_id)
    if cur_user == None:
        cur_user = Users(chat_id, call.message.json["from"])

    tmp = call.data.split("|")
    menu = tmp[0] if len(tmp) > 0 else ""
    cmd = tmp[1] if len(tmp) > 1 else ""
    par = tmp[2] if len(tmp) > 2 else ""

    if menu == "GameRPSm":

        if cmd == "newGame":
            # bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)  # удалим кнопки начала игры из чата
            bot.delete_message(chat_id, message_id)
            botGames.newGame(chat_id, botGames.GameRPS_Multiplayer(bot, cur_user))
            bot.answer_callback_query(call.id)

        elif cmd == "Join":
            # bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)  # удалим кнопки начала игры из чата
            bot.delete_message(chat_id, message_id)
            gameRSPMult = Menu.getExtPar(par)
            if gameRSPMult is None:  # если наткнулись на кнопку, которой быть не должно
                return
            else:
                gameRSPMult.addPlayer(cur_user.id, cur_user.userName)
            bot.answer_callback_query(call.id)

        elif cmd == "Exit":
            bot.delete_message(chat_id, message_id)
            gameRSPMult = Menu.getExtPar(par)
            if gameRSPMult is not None:
                gameRSPMult.delPlayer(cur_user.id)
            menuBot.goto_menu(bot, chat_id, "Игры")
            bot.send_message(chat_id, "Вы находитесь в меню игры", reply_markup=Menu.getMenu(chat_id, cm.dict["games"]).markup)
            bot.answer_callback_query(call.id)

        elif "Choice-" in cmd:
            gameRSPMult = Menu.getExtPar(par)
            if gameRSPMult is None:  # если наткнулись на кнопку, которой быть не должно - удалим её из чата
                bot.delete_message(chat_id, message_id)
            else:
                choice = cmd[7:]
                gameRSPMult.playerChoice(cur_user.id, choice)
            bot.answer_callback_query(call.id)

    elif menu == "Wordle_m":

        if cmd == "newGame":
            # bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)  # удалим кнопки начала игры из чата
            bot.delete_message(chat_id, message_id)
            botGames.newGame(chat_id, botGames.Wordle_Multiplayer(bot, cur_user))
            bot.answer_callback_query(call.id)

        elif cmd == "Join":
            # bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)  # удалим кнопки начала игры из чата
            bot.delete_message(chat_id, message_id)
            Wordle_Mult = Menu.getExtPar(par)
            if Wordle_Mult is None:  # если наткнулись на кнопку, которой быть не должно
                return
            else:
                Wordle_Mult.addPlayer(cur_user.id, cur_user.userName)
            bot.answer_callback_query(call.id)

        elif cmd == "Exit":
            bot.delete_message(chat_id, message_id)
            Wordle_Mult = Menu.getExtPar(par)
            if Wordle_Mult is not None:
                Wordle_Mult.delPlayer(cur_user.id)
            menuBot.goto_menu(bot, chat_id, cm.dict["games"])
            bot.send_message(chat_id, "Вы находитесь в меню игры", reply_markup=Menu.getMenu(chat_id, cm.dict["games"]).markup)
            bot.answer_callback_query(call.id)


# -----------------------------------------------------------------------



# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias

# -----------------------------------------------------------------------
def send_help(chat_id):
    global bot
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Написать автору", url="https://t.me/GreatFireDragon")
    markup.add(btn1)
    try:
        bot.send_photo(chat_id,
                       'https://static.independent.co.uk/2021/06/16/08/newFile-4.jpg?quality=75&width=982&height=726&auto=webp',
                       caption="Автор: Кулешов МС 1МД25", reply_markup=markup)
    except Exception:
        bot.send_photo(chat_id,
                       open('images/tea.jpg', "rb"),
                       caption="Автор: Кулешов МС 1МД25", reply_markup=markup)

# -----------------------------------------------------------------------
def send_film(chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)

# ---------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm

# -----------------------------------------------------------------------
def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
    result_find = soup.select('.anekdot_text')
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]


# -----------------------------------------------------------------------
# Функция, которая отпарвляет "Пришлите фото для обработки"
def send_photo_please(message):
    global operation  # Для обработки фото делаем глобальной

    operation = message.text
    msg = bot.reply_to(message, text="Пришлите фото для обработки")
    bot.register_next_step_handler(msg, photo_step)

# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Обработка изображений
def photo_step(message):

    chat_id = message.chat.id
    global operation

    try:
        fileID = message.photo[-1].file_id
    except Exception:
        msg = bot.send_message(chat_id, text="Ошибка! Пришлите фото!")
        bot.register_next_step_handler(msg, photo_step)
        return


    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("input_image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    if operation == cm.dict["blur"]:

        stringList = (10, 20)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for value in stringList:
            btn = types.KeyboardButton(str(value))
            markup.add(btn)

        msg = bot.reply_to(message, "Выберите степень блюра (Или напишите своё целое число)", reply_markup=markup)
        bot.register_next_step_handler(msg, ocv.blur_matrix_step)

    elif operation == cm.dict["ch_b"]:
        ocv.chb("input_image.jpg")
        ocv.all_done_photo(chat_id)

    elif operation == cm.dict["canny"]:

        stringList = (50, 100, 200)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for value in stringList:
            btn = types.KeyboardButton(str(value))
            markup.add(btn)

        msg = bot.reply_to(message, "Выберите параметр выделения краёв (Или напишите своё целое число)", reply_markup=markup)
        bot.register_next_step_handler(msg, ocv.canny_matrix_step)

    elif operation == cm.dict["mirror"]:
        ocv.mirror_y("input_image.jpg")
        ocv.all_done_photo(chat_id)

    elif operation == cm.dict["mirror2"]:
        ocv.mirror_x("input_image.jpg")
        ocv.all_done_photo(chat_id)

    elif operation == cm.dict["cartoon"]:

        stringList = (8, 16, 24)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for value in stringList:
            btn = types.KeyboardButton(str(value))
            markup.add(btn)

        msg = bot.reply_to(message, "Выберите количество цветов (Или напишите своё целое число)",
                           reply_markup=markup)
        bot.register_next_step_handler(msg, ocv.cartoon_matrix_step)

    else:
        return



# -----------------------------------------------------------------------


bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()
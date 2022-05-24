from telebot import types
import commands as cm
import pickle
import os


# -----------------------------------------------------------------------
class KeyboardButton:
    def __init__(self, name, handler=None):
        self.name = name
        self.handler = handler

# -----------------------------------------------------------------------
class Users:
    activeUsers = {}

    def __init__(self, chat_id, user_json):
        self.id = user_json["id"]
        self.isBot = user_json["is_bot"]
        self.firstName = user_json["first_name"]
        self.userName = user_json["username"]
        self.languageCode = user_json.get("language_code", "")
        self.__class__.activeUsers[chat_id] = self

    def __str__(self):
        return f"Name user: {self.firstName}   id: {self.userName}   lang: {self.languageCode}"

    def getUserHTML(self):
        return f"Name user: {self.firstName}   id: <a href='https://t.me/{self.userName}'>{self.userName}</a>   lang: {self.languageCode}"

    @classmethod
    def getUser(cls, chat_id):
        return cls.activeUsers.get(chat_id)


# -----------------------------------------------------------------------
class Menu:
    hash = {}  # тут будем накапливать все созданные экземпляры класса
    cur_menu = {}  # тут будет находиться текущий экземпляр класса, текущее меню для каждого пользователя
    extendedParameters = {}  # это место хранения дополнительных параметров для передачи в inline кнопки
    namePickleFile = "bot_curMenu.plk"

    # ПЕРЕПИСАТЬ для хранения параметров привязанных к chat_id и названию кнопки

    def __init__(self, name, buttons=None, parent=None, handler=None):
        self.parent = parent
        self.name = name
        self.buttons = buttons
        self.handler = handler

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
        markup.add(*buttons)  # Обратите внимание - звёздочка используется для распаковки списка
        self.markup = markup

        self.__class__.hash[name] = self  # в классе содержится словарь, со всеми экземплярами класса, обновим его

    @classmethod
    def getExtPar(cls, id):
        return cls.extendedParameters.pop(id, None)

    @classmethod
    def setExtPar(cls, parameter):
        import uuid
        id = uuid.uuid4().hex
        cls.extendedParameters[id] = parameter
        return id

    @classmethod
    def getMenu(cls, chat_id, name):
        menu = cls.hash.get(name)
        if menu != None:
            cls.cur_menu[chat_id] = menu
        return menu

    @classmethod
    def getCurMenu(cls, chat_id):
        return cls.cur_menu.get(chat_id)


# -----------------------------------------------------------------------
def goto_menu(bot, chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == cm.dict["exit"] and cur_menu != None and cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)
        return target_menu
    else:
        return None

# -----------------------------------------------------------------------

m_main = Menu(cm.dict["main_menu"], buttons=[cm.dict["fun"], cm.dict["games"], cm.dict["DZ"], cm.dict["stat"], cm.dict["images"], cm.dict["help"]])

m_games = Menu(cm.dict["games"], buttons=[cm.dict["rsp"], cm.dict["rsp_m"], cm.dict["21"], cm.dict["wordle"], cm.dict["exit"]], parent=m_main)

m_game_21 = Menu(cm.dict["21"], buttons=[cm.dict["card"], cm.dict["stop"], cm.dict["exit"]], parent=m_games, handler="game_21")
m_game_rsp = Menu(cm.dict["rsp"], buttons=[cm.dict["rock"], cm.dict["paper"], cm.dict["scissors"], cm.dict["exit"]], parent=m_games, handler="game_rsp")
m_game_wordle = Menu(cm.dict["wordle"], buttons=[cm.dict["full_pattern"], cm.dict["exit"]], parent=m_games, handler="game_wordle")


m_DZ = Menu(cm.dict["DZ"], buttons=[cm.dict["№1"], cm.dict["№2"], cm.dict["№3"], cm.dict["№4"],
                                    cm.dict["№5"], cm.dict["№6"], cm.dict["№7"], cm.dict["exit"]], parent=m_main)

m_fun = Menu(cm.dict["fun"], buttons=[cm.dict["cat"], cm.dict["human"], cm.dict["joke"], cm.dict["pony"],
                                      cm.dict["movie"], cm.dict["exit"]], parent=m_main)

m_stat = Menu(cm.dict["stat"], buttons=[cm.dict["news"], cm.dict["valute"], cm.dict["exit"]], parent=m_main )

m_images = Menu(cm.dict["images"], buttons=[cm.dict["blur"], cm.dict["ch_b"], cm.dict["canny"],
                                            cm.dict["mirror"], cm.dict["mirror2"], cm.dict["cartoon"], cm.dict["exit"]], parent=m_main)

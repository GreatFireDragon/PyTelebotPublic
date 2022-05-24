import telebot
from telebot import types
import requests
import os
import random

API_KEY = '5263831940:AAGxk7T_bP7eQGDmKeH6sopuVCH7dpY_8bo'
bot = telebot.TeleBot(API_KEY)

cmonya = 0   # CHMONYA

def send_cat(message):
    chat_id = message.chat.id

    url = 'http://thiscatdoesnotexist.com'
    pic = url[7:] + '.jpg'
    r = requests.get(url, allow_redirects=True)
    open(pic, 'wb').write(r.content)

    global cmonya
    cmonya += 1

    if cmonya == 5:
        bot.send_photo(chat_id,
                       open("images/chmonya.jpg", "rb"),
                       caption="Вы разблокировали чмоню!",
                       # reply_markup=markup
                       )
    else:
        bot.send_photo(chat_id,
                       open(pic, "rb"),
                       caption="Держи кота. Хочешь ещё?",
                       # reply_markup=markup
                       )

    # os.remove(pic)


def send_person(message):
    chat_id = message.chat.id

    url = 'https://thispersondoesnotexist.com/image'
    pic = 'image.jpg'
    r = requests.get(url, allow_redirects=True)
    open(pic, 'wb').write(r.content)

    # markup.add(btn2, back)

    bot.send_photo(chat_id,
                   open(pic, "rb"),
                   caption="Держи человека. Хочешь ещё?",
                   # reply_markup=markup
                   )

    # os.remove(pic)

def send_pony(chat_id):
    pone_seed = str(random.randrange(10000, 99999))
    pone_seed = 'https://thisponydoesnotexist.net/v1/w2x-redo/jpgs/seed' + pone_seed + '.jpg'

    bot.send_photo(chat_id, pone_seed, caption="")
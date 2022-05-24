import re

# -----------------------------------------------------------------------
def dz1(bot, chat_id):
    my_name, my_age = "Михаил", 19
    my_name_X5 = (my_name + " ") * 5
    bot.send_message(chat_id, "Имя: %s, Возраст %s, \nИмя повторённое 5 раз: %s" % (my_name, my_age, my_name_X5))
# -----------------------------------------------------------------------
def dz2(bot, chat_id):
    age_answer = lambda message, joke: bot.send_message(chat_id, f"{joke} {message.text}? \nТянешь на все {round(int(message.text) / 2)}!")
    age_check = lambda message: age_answer(message, "Целых") if (int(correct_age(bot, chat_id, message.text)) <= 18) else age_answer(message, "Всего")
    qwerty = lambda message: my_input(bot, chat_id, f"Привет, {correct_name(bot, chat_id, message.text)}  \nСколько тебе лет?", age_check)
    my_input(bot, chat_id, "Как тебя зовут?", qwerty)
# -----------------------------------------------------------------------
def dz3(bot, chat_id):
    qwerty = lambda message: bot.send_message(chat_id, "{}\n{}\n{}\n{}".format(message.text[1:-1], message.text[::-1],
                                                                               message.text[-3:], message.text[:5]))
    my_input(bot, chat_id, "Как тебя зовут?", qwerty)
# -----------------------------------------------------------------------
def dz4(bot, chat_id):
    qwerty = lambda message: bot.send_message(chat_id,
                                              f"В твоём имени {len(message.text)} букв!")
    my_input(bot, chat_id, "Как тебя зовут?", qwerty)

# -----------------------------------------------------------------------
def dz5(bot, chat_id):
    mult = lambda x: int(x[0]) * int(x[1])
    addit = lambda x: int(x[0]) + int(x[1])
    age_ans = lambda message: bot.send_message(chat_id, "Произведение цифр твоего возраста: {}\nСумма цифр твоего вораста: {}".format(mult(message.text), addit(message.text)))

    my_input(bot, chat_id, "Сколько тебе лет?", age_ans)
# -----------------------------------------------------------------------
def dz6(bot, chat_id):
    qwerty = lambda message: bot.send_message(chat_id, "{}\n{}\n{}\n{}".format(message.text.upper(), message.text.lower(),
                                                                               message.text.capitalize(),
                                                                               message.text[0].lower() + message.text[1:].upper()))
    my_input(bot, chat_id, "Как тебя зовут?", qwerty)
# -----------------------------------------------------------------------
def dz7(bot, chat_id):
    proc_answer = lambda message: bot.send_message(chat_id, "Абсолютно точно верно, да, да, ты угадал!") if (message.text == "1") else bot.send_message(chat_id, "Нет, лол")
    my_input(bot, chat_id, "Чему равен натуральный логарифм числа \"e\"? ", proc_answer)


    # proc_answer = lambda message: bot.send_message(chat_id, f"Добро пожаловать {message.text}! У тебя красивое имя, в нём {len(message.text)} букв!")
    # my_input(bot, chat_id, "Как тебя зовут?", proc_answer)

# -----------------------------------------------------------------------
def my_input(bot, chat_id, txt, proc_answer):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, proc_answer)



# -----------------------------------------------------------------------
def correct_name(bot, chat_id, name):
    if not len(re.findall("[A-Za-zА-Яа-я]", name)) == len(name):
        bot.send_message(chat_id, "\n ош-ш...\nОШИБКА!\n \nПожалуйста, напишите только имя без пробелов")
        raise quit()
    else:
        return name
# -----------------------------------------------------------------------
def correct_age(bot, chat_id, age):
    try: age = int(age)
    except Exception:
        bot.send_message(chat_id, "Пожалуйста, попробуйте ещё раз. И напишите ваш возраст в виде целого числа. \n например, 15")
        raise quit()

    if age < 0 or age > 150:
        bot.send_message(chat_id, f"Пожалуйста, попробуйте ещё раз. И честно напишите ваш возраст. \nВам не может быть {age} лет/года")
        raise quit()
    else: return age
# -----------------------------------------------------------------------
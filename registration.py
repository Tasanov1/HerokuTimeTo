import psycopg2
from telegram import ReplyKeyboardMarkup
from keyboards import *
from pytz import all_timezones
import pytz
from pytz import timezone
from telegram.ext import ConversationHandler
from main import *
from keyboards import *

NAME, BIRTH, CITY, INSTA, STUDY, JOB, HOBBY, GOALS, TYPE, TIMEZONE, PAGE= range(11)

def askName(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    chat_id = update.message.chat_id
    text = update.message.text
    user = update.message.from_user.name
    cursor.execute("INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (chat_id, text, "*", "*", "*", "*", "*", "*", user, "*", '*', '*'))
    conn.commit()
    sendMessage(bot, update, '*Дата рождения:*\n(в формате dd/mm/yyyy, 01/01/2019)')
    return BIRTH

def askBirth(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    chat_id = update.message.chat_id
    text = update.message.text
    if len(text) != 10:
        return BIRTH
    d = int(text[:-8])
    m = int(text[3:-5])
    y = int(text[6:])
    year = datetime.datetime.now().year
    if d > 31 or d < 1 or m < 1 or m > 12 or y > year or y < 1934:
        sendMessage(bot, update, 'Пожалуйста, введите в правильном формате.\n(в формате dd/mm/yyyy, 01/01/2019)')
        return BIRTH
    else:
        cursor.execute("UPDATE Users SET birth = %s WHERE chat_id = %s", [text, chat_id])
        conn.commit()
        sendMessage(bot, update, "В каком *Городе* вы живете?")
        return CITY

def askCity(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    chat_id = update.message.chat_id
    text = update.message.text
    cursor.execute("UPDATE Users SET city = %s WHERE chat_id = %s", [text, chat_id])
    conn.commit()
    sendMessage(bot, update, "*Insta:*\n(Если нет инсты, напишите просто нет)")
    return INSTA

def askInsta(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    chat_id = update.message.chat_id
    text = update.message.text
    text = text.replace('@', '')
    cursor.execute("UPDATE Users SET insta = %s WHERE chat_id = %s", [text, chat_id])
    conn.commit()
    sendMessage(bot, update, "*Место учебы:*")
    return STUDY

def askStudy(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    chat_id = update.message.chat_id
    text = update.message.text
    cursor.execute("UPDATE Users SET study = %s WHERE chat_id = %s", [text, chat_id])
    conn.commit()
    sendMessage(bot, update, "*Место работы:*\n(Если не работаете, напишите просто нет)")
    return JOB

def askJob(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    chat_id = update.message.chat_id
    text = update.message.text
    cursor.execute("UPDATE Users SET job = %s WHERE chat_id = %s", [text, chat_id])
    conn.commit()
    sendMessage(bot, update, "*Хобби:*")
    return HOBBY

def askHobby(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    chat_id = update.message.chat_id
    text = update.message.text
    cursor.execute("UPDATE Users SET hobby = %s WHERE chat_id = %s", [text, chat_id])
    conn.commit()
    sendMessage(bot, update, "*Цель:*")
    return GOALS

def askGoals(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    chat_id = update.message.chat_id
    text = update.message.text
    cursor.execute("UPDATE Users SET goals = %s WHERE chat_id = %s", [text, chat_id])
    conn.commit()

    update.message.reply_text("Выберите навыки. Затем нажмите на кнопку 'send'", reply_markup=choose_keyboard())
    return ConversationHandler.END

def update_keyboard(bot, query, text):
    chat_id = query.message.chat_id
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CheckBox")
    all = cursor.fetchall()
    ans = ['design', 'web development', 'mobile development', 'data science', 'language', 'filmmaking', 'photography', 'marketing', 'finance', 'management', 'dance', 'music', 'art', 'sport', 'oratory', 'stylist', 'startup', 'hardware', 'psychology', 'hiking', 'games', 'travel', 'send']
    ans2 = []
    keyboard = []
    for i in all:
        if i[0] == chat_id:
            ans2.append(i[1])
    k = [i for i in ans if not i in ans2]
    for i in k:
        keyboard.append([InlineKeyboardButton(i, callback_data=i)])
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text="Выберите навыки. Затем нажмите на кнопку 'send'",
                          reply_markup=InlineKeyboardMarkup(keyboard))

def askType(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CheckBox")
    all = cursor.fetchall()
    query = update.callback_query
    chat_id = query.message.chat_id
    data = str(query.data)
    text = ""

    if data == 'send':
        for i in all:
            if i[0] == chat_id:
                text += str(i[1]) + '\n'
                cursor.execute("DELETE FROM CheckBox WHERE chat_id = %s", [chat_id])
                conn.commit()
    else:
        check = False
        user = False
        for i in all:
            if i[0] == chat_id:
                user = True
        for i in all:
            if i[1] == data and i[0] == chat_id:
                check = True
        if user == False or check == False:
            cursor.execute("INSERT INTO CheckBox VALUES(%s,%s)", (chat_id, data))
            conn.commit()

    if not '\n' in text:
        update_keyboard(bot, query, text)

    else:
        cursor.execute("UPDATE Users SET type = %s WHERE chat_id = %s", [text, chat_id])
        conn.commit()
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text="Спасибо!")
        sendMessage(bot, query, "Введите *часовой пояс:*\n(в таком формате +06:00, +05:00, -06:00. +03:00))")

        return TIMEZONE

def askTimezone(bot, update):
    now_utc = datetime.datetime.now(pytz.timezone('UTC'))
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    chat_id = update.message.chat_id
    user = update.message.from_user.name
    check = False
    text = str(update.message.text)
    zones = []
    if len(text) == 6:
        for i in all_timezones:
            if text in str(now_utc.astimezone(pytz.timezone(i))):
                zones.append(i)
    if len(zones) != 0:
        check = True
    if check:
        cursor.execute("UPDATE Users SET timezone = %s WHERE chat_id = %s", [zones[0], chat_id])
        conn.commit()
        cursor.execute("INSERT INTO WakeUp VALUES (%s, %s, %s, %s)",(user, chat_id, 1, "*"))
        conn.commit()
        cursor.execute("INSERT INTO Scribing VALUES (%s, %s, %s, %s)", (user, chat_id, 1, "*"))
        conn.commit()
        cursor.execute("INSERT INTO Visualization VALUES (%s, %s, %s, %s)", (user, chat_id, 1, "*"))
        conn.commit()
        cursor.execute("INSERT INTO Extra VALUES (%s, %s, %s, %s, %s)", (user, chat_id, 1, "*", '*'))
        conn.commit()
        cursor.execute("INSERT INTO Exercise VALUES (%s, %s, %s, %s, %s)", (user, chat_id, 1, "*", '*'))
        conn.commit()
        cursor.execute("INSERT INTO Expert VALUES (%s, %s, %s, %s, %s)", (user, chat_id, 1, "*", '*'))
        conn.commit()
        cursor.execute("INSERT INTO Reading VALUES (%s, %s, %s, %s, %s, %s)", (user, chat_id, 1, "*", '*', 0))
        conn.commit()
        update.message.reply_text("Добро пожаловать!", reply_markup=main_menu_keyboard())
        bot.send_message(-1001184336722, getInfo(update.message.chat_id))
        #1001184336722
        return ConversationHandler.END
    else:
        update.message.reply_text("Пожалуйста, попробуйте ввести часовой пояс в правильном формате.\n(+06:00, +05:00, -06:00. +03:00)")
        return TIMEZONE

def askInsight(bot, update):
    text = update.message.text
    bot.send_message(-1001436164632, text)
    sendMessage(bot, update, 'Ваш инсайт отправлен!')
    return ConversationHandler.END

def askExercise(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    all = cursor.fetchall()
    for i in all:
        if i[0] == chat_id:
            zone = i[9]
    cursor.execute("SELECT * FROM Exercise")
    arr = cursor.fetchall()
    for i in arr:
        if i[1] == chat_id:
            point = i[2]
    now_utc = datetime.datetime.now(pytz.timezone('UTC'))
    current = now_utc.astimezone(timezone(zone))
    cursor.execute("UPDATE Exercise SET lastday = %s, point = %s, text = %s WHERE chat_id = %s",
                   [current, point * 2, text, chat_id])
    text = 'Круто! Ваш пойнт: ' + str(point * 2)
    conn.commit()
    update.message.reply_text(text)
    return ConversationHandler.END

def askExpert(bot, update):
    chat_id = update.message.chat_id
    ex = update.message.text
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    all = cursor.fetchall()
    for i in all:
        if i[0] == chat_id:
            zone = i[9]
    now_utc = datetime.datetime.now(pytz.timezone('UTC'))
    current = now_utc.astimezone(timezone(zone))
    cursor.execute("SELECT * FROM Expert")
    arr = cursor.fetchall()
    point = 1
    for i in arr:
        if i[1] == chat_id:
            point = i[2]
            cursor.execute("UPDATE Expert SET lastday = %s, point = %s, text = %s WHERE chat_id = %s", [current, point * 2, ex, chat_id])
            text = 'Круто! Ваш пойнт: ' + str(point * 2)
            conn.commit()
    update.message.reply_text(text)
    return ConversationHandler.END

def askExtra(bot, update):
    chat_id = update.message.chat_id
    ex = update.message.text
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    all = cursor.fetchall()
    for i in all:
        if i[0] == chat_id:
            zone = i[9]
    now_utc = datetime.datetime.now(pytz.timezone('UTC'))
    current = now_utc.astimezone(timezone(zone))
    cursor.execute("SELECT * FROM Extra")
    arr = cursor.fetchall()
    point = 1
    for i in arr:
        if i[1] == chat_id:
            point = i[2]
            cursor.execute("UPDATE Extra SET lastday = %s, point = %s, text = %s WHERE chat_id = %s", [current, point * 2, ex, chat_id])
            text = 'Круто! Ваш пойнт: ' + str(point * 2)
            conn.commit()
    update.message.reply_text(text)
    return ConversationHandler.END

def getInfo(chat_id):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    arr = cursor.fetchall()
    now_utc = datetime.datetime.now(pytz.timezone('UTC'))
    text = ''
    for i in arr:
        if i[0] == chat_id:
            tz = str(now_utc.astimezone(pytz.timezone(i[9])))[26:]
            text = '*Имя Фамилия: *' + i[1] + '\n*Дата рождения: *' + i[2] + '\n*Город: *' + i[10] + '\n*Insta:* instagram.com/' + i[11] + '\n*Место учебы:* ' + i[3] + '\n*Место работы: *' + i[4] + '\n*Хобби:* ' + i[5] + '\n*Цель:* ' + i[6] + '\n*Направления:*\n' + i[7] + '*Ссылка:* ' + i[8] + '\n*Часовой пояс:* ' + tz
    return text
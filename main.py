import telegram
import psycopg2
import constants
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
import keyboards
import time
#import registration
from telegram.ext import MessageHandler, Filters
import datetime
from pytz import all_timezones
import pytz
from pytz import timezone
TOKEN = constants.token
NAME, BIRTH, CITY, INSTA, STUDY, JOB, HOBBY, GOALS, TYPE, TIMEZONE, EXERCISE, EXTRA, EXPERT, INSIGHT, BOOK, PAGE, LEADERBOARD = range(17)

conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
cursor = conn.cursor()
cursor.execute("""
        SELECT *
        FROM Users
    """)
users = cursor.fetchall()
def sendMessage(bot, update, text, reply_markup=None):
    if(reply_markup):
        reply_markup = InlineKeyboardMarkup(reply_markup)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=telegram.ParseMode.MARKDOWN
    )

def leaderboard(bot, update):
    chat_id = update.message.chat_id
    if chat_id == 488113841 or chat_id == 94762933:
        conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
        cursor = conn.cursor()
        chat_id = update.message.chat_id
        cursor.execute("SELECT * FROM WakeUp ORDER BY point DESC")
        wakeup = cursor.fetchall()
        cursor.execute("SELECT * FROM Scribing ORDER BY point DESC")
        scribing = cursor.fetchall()
        cursor.execute("SELECT * FROM Visualization ORDER BY point DESC")
        vis = cursor.fetchall()
        cursor.execute("SELECT * FROM Extra ORDER BY point DESC")
        extra = cursor.fetchall()
        cursor.execute("SELECT * FROM Expert ORDER BY point DESC")
        expert = cursor.fetchall()
        cursor.execute("SELECT * FROM Exercise ORDER BY point DESC")
        exercise = cursor.fetchall()
        cursor.execute("SELECT * FROM Reading ORDER BY point DESC")
        reading = cursor.fetchall()
        text = '#wakeup: \n'
        t = 1
        for i in wakeup:
            if(t < 6):
                text += str(t) + '. ' + i[0] + ' point: ' + str(i[2]) + '\n'
                t=t+1
        text += '#scribing: \n'
        t = 1
        for i in scribing:
            if (t < 6):
                text += str(t) + '. ' + i[0] + ' point: ' + str(i[2]) + '\n'
                t = t + 1
        text += '#visualization: \n'
        t = 1
        for i in vis:
            if (t < 6):
                text += str(t) + '. ' + i[0] + ' point: ' + str(i[2]) + '\n'
                t = t + 1
        text += '#extra: \n'
        t = 1
        for i in extra:
            if (t < 6):
                text += str(t) + '. ' + i[0] + ' point: ' + str(i[2]) + '\n'
                t = t + 1
        text += '#expert: \n'
        t = 1
        for i in expert:
            if (t < 6):
                text += str(t) + '. ' + i[0] + ' point: ' + str(i[2]) + '\n'
                t = t + 1
        text += '#exercise: \n'
        t = 1
        for i in exercise:
            if (t < 6):
                text += str(t) + '. ' + i[0] + ' point: ' + str(i[2]) + '\n'
                t = t + 1
        text += '#reading: \n'
        t = 1
        for i in reading:
            if (t < 6):
                text += str(t) + '. ' + i[0] + ' point: ' + str(i[2]) + '\n'
                t = t + 1
        cursor.execute("SELECT * FROM Users")
        users = cursor.fetchall()
        count = len(users)
        text += 'Количество участников: ' + str(count)
        sendMessage(bot, update, text)

def cancel(bot, update):
    sendMessage(bot, update, 'Отмена')
    return ConversationHandler.END

def help(bot, update):
    sendMessage(bot, update, '/start - команда для вызова меню\n/help - помощь по командам\n/cancel - отмена')

def start(bot, update):
    user = update.message.from_user.name
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM Users
    """)
    users = cursor.fetchall()
    del_id = -1
    for i in range(0, len(users)):
        for j in range(0, 11):
            if users[i][j] == -1 or users[i][j] == '*':
                del_id = users[i][0]
    if del_id != -1:
        cursor.execute("DELETE FROM Users WHERE chat_id = %s", [del_id])
        conn.commit()
        cursor.execute("DELETE FROM WakeUp WHERE chat_id = %s", [del_id])
        conn.commit()
        cursor.execute("DELETE FROM Scribing WHERE chat_id = %s", [del_id])
        conn.commit()
        cursor.execute("DELETE FROM Visualization WHERE chat_id = %s", [del_id])
        conn.commit()
        cursor.execute("DELETE FROM Extra WHERE chat_id = %s", [del_id])
        conn.commit()
        cursor.execute("DELETE FROM Expert WHERE chat_id = %s", [del_id])
        conn.commit()
        cursor.execute("DELETE FROM Exercise WHERE chat_id = %s", [del_id])
        conn.commit()
        cursor.execute("DELETE FROM Reading WHERE chat_id = %s", [del_id])
        conn.commit()
        cursor.execute("""
                SELECT *
                FROM Users
            """)
        users = cursor.fetchall()
    chat_id = update.message.chat_id
    check = False
    for i in users:
        if i[0] == chat_id:
            check = True
    if check:
        update.message.reply_text("Добро пожаловать! " + user, reply_markup=keyboards.main_menu_keyboard())
    else:
        sendMessage(bot, update, "Привет! Я #timetoBot. \nПожалуйста, пройдите регистрацию! \n*Имя и Фамилия:*")
        return NAME

def main_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text="Меню",
                        reply_markup=keyboards.main_menu_keyboard())

def first_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            text="#challenge",
                            reply_markup=keyboards.first_menu_keyboard())

def second_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            text="#skills",
                            reply_markup=keyboards.second_menu_keyboard())

def statistics(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    query = update.callback_query
    chat_id = query.message.chat_id
    text = ""
    cursor.execute("SELECT * FROM WakeUp")
    wakeup = cursor.fetchall()
    cursor.execute("SELECT * FROM Scribing")
    scribing = cursor.fetchall()
    cursor.execute("SELECT * FROM Visualization")
    vis = cursor.fetchall()
    cursor.execute("SELECT * FROM Extra")
    extra = cursor.fetchall()
    cursor.execute("SELECT * FROM Expert")
    expert = cursor.fetchall()
    cursor.execute("SELECT * FROM Exercise")
    exercise = cursor.fetchall()
    cursor.execute("SELECT * FROM Reading")
    reading = cursor.fetchall()
    for i in wakeup:
        if i[1] == chat_id:
            text+='#wakeup: ' + i[3][:-16] + ', points: ' + str(i[2])
    for i in scribing:
        if i[1] == chat_id:
            text+='\n#scribing: ' + i[3][:-16] + ', points: ' + str(i[2])
    for i in vis:
        if i[1] == chat_id:
            text+='\n#visualization: ' + i[3][:-16] + ', points: ' + str(i[2])
    for i in extra:
        if i[1] == chat_id:
            text += '\n#extra: ' + i[3][:-16]+ ',' + i[4] + ', points: ' + str(i[2])
    for i in expert:
        if i[1] == chat_id:
            text += '\n#expert: ' + i[3][:-16]+ ',' + i[4] + ', points: ' + str(i[2])
    for i in exercise:
        if i[1] == chat_id:
            text += '\n#exercise: ' + i[3][:-16]+ ',' + i[4] + ', points: ' + str(i[2])
    for i in reading:
        if i[1] == chat_id:
            text += '\n#reading: ' + i[3][:-16]+ ', book: ' + i[4] + ', pages: ' + str(i[5]) + ', points: ' + str(i[2])
    sendMessage(bot, query, 'Статистика: \n' + text)

def profile(bot, update):
    query = update.callback_query
    sendMessage(bot, query, registration.getInfo(query.message.chat_id))

def insight(bot, update):
    query = update.callback_query
    sendMessage(bot, query, 'Свой инсайт: ')
    return INSIGHT

def search(type):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT *
                    FROM Users
                """)
    all = cursor.fetchall()
    text = "Список участников по направлениям. Вы можете свзяаться с ними и задать непонятные вам вопросы:\n" + '*' + type[1:] + '*' + "\n"
    check = False

    for i in all:
        if type[1:] in i[7]:
            text += i[8] + '\n'
            check = True

    if check == False:
        text += "Список пуст"
    return text

def skills(bot, update):
    query = update.callback_query
    type = str(query.data)
    text = search(type)
    sendMessage(bot, query, text)

def everyDay(current, option, chat_id):
    minute = int(current.hour)*60+current.minute
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    if option == 'wakeup':
        cursor.execute("SELECT * FROM WakeUp")
        arr = cursor.fetchall()
    elif option == 'scribing':
        cursor.execute("SELECT * FROM Scribing")
        arr = cursor.fetchall()
    elif option == 'visualization':
        cursor.execute("SELECT * FROM Visualization")
        arr = cursor.fetchall()
    check = -1
    point = 1
    lastday = ''
    for i in arr:
        if i[1] == chat_id:
            point = i[2]
            if i[3] == '*':
                check = 0
            elif i[3] != '*':
                lastday = str(i[3])[8:-19]
                check = 1
    print(lastday)
    print(minute)
    if check == 0:
        if option == 'wakeup':
            if minute > 235 and minute < 300:
                cursor.execute("UPDATE WakeUp SET lastday = %s, point = %s WHERE chat_id = %s",
                               [current, point * 2, chat_id])
                text = 'Доброе утро!' + str(current.hour) + ':' + str(current.minute) + 'Ваш пойнт: ' + str(point * 2)
            elif minute > 300 and minute < 360:
                cursor.execute("UPDATE WakeUp SET lastday = %s, point = %s WHERE chat_id = %s",
                               [current, point, chat_id])
                text = 'Доброе утро!' + str(current.hour) + ':' + str(current.minute) + 'Ваш пойнт: ' + str(point * 2)
            elif minute > 360:
                cursor.execute("UPDATE WakeUp SET lastday = %s, point = %s WHERE chat_id = %s",
                               [current, 1, chat_id])
                text = 'Доброе утро!' + str(current.hour) + ':' + str(current.minute) + 'Ваш пойнт: 1'
        elif option == 'scribing':
            cursor.execute("UPDATE Scribing SET lastday = %s, point = %s WHERE chat_id = %s", [current, point * 2, chat_id])
            text = 'Круто! Ваш пойнт: ' + str(point * 2)
        elif option == 'visualization':
            cursor.execute("UPDATE Visualization SET lastday = %s, point = %s WHERE chat_id = %s", [current, point * 2, chat_id])
            text = 'Круто! Ваш пойнт: ' + str(point * 2)
        conn.commit()

    elif check == 1:
        if lastday < str(current.day):
            if option == 'wakeup':
                if minute > 235 and minute < 300:
                    cursor.execute("UPDATE WakeUp SET lastday = %s, point = %s WHERE chat_id = %s",
                                   [current, point * 2, chat_id])
                    text = 'Доброе утро!' + str(current.hour) + ':' + str(current.minute) + 'Ваш пойнт: ' + str(
                        point * 2)
                elif minute > 300 and minute < 360:
                    cursor.execute("UPDATE WakeUp SET lastday = %s, point = %s WHERE chat_id = %s",
                                   [current, point, chat_id])
                    text = 'Доброе утро!' + str(current.hour) + ':' + str(current.minute) + 'Ваш пойнт: ' + str(
                        point * 2)
                elif minute > 360:
                    cursor.execute("UPDATE WakeUp SET lastday = %s, point = %s WHERE chat_id = %s",
                                   [current, 1, chat_id])
                    text = 'Доброе утро!' + str(current.hour) + ':' + str(current.minute) + 'Ваш пойнт: 1'
            elif option == 'scribing':
                cursor.execute("UPDATE Scribing SET lastday = %s, point = %s WHERE chat_id = %s",
                               [current, point * 2, chat_id])
                text = 'Круто! Ваш пойнт: ' + str(point * 2)
            elif option == 'visualization':
                cursor.execute("UPDATE Visualization SET lastday = %s, point = %s WHERE chat_id = %s",
                               [current, point * 2, chat_id])
                text = 'Круто! Ваш пойнт: ' + str(point * 2)
            conn.commit()
        else:
            text = 'Попробуйте через день. Ваш пойнт: ' + str(point)
    return text

def options(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    option = str(query.data)
    text = ""
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    all = cursor.fetchall()
    for i in all:
        if i[0] == chat_id:
            zone = i[9]
    now_utc = datetime.datetime.now(pytz.timezone('UTC'))
    current = now_utc.astimezone(timezone(zone))

    if option == "wakeup":
        text = everyDay(current, option, chat_id)
        sendMessage(bot, query, text)
    elif option == "scribing":
        text = everyDay(current, option, chat_id)
        sendMessage(bot, query, text)
    elif option == 'visualization':
        text = everyDay(current, option, chat_id)
        sendMessage(bot, query, text)
    elif option == 'exercise':
        cursor.execute("SELECT * FROM Exercise")
        arr = cursor.fetchall()
        check = -1
        lastday = ''
        for i in arr:
            if i[1] == chat_id:
                if i[3] == '*':
                    check = 0
                elif i[3] != '*':
                    point = i[2]
                    lastday = str(i[3])[8:-19]
                    check = 1
        if check == 0:
            sendMessage(bot, query, 'Какие упражнения делали?')
            return EXERCISE
        elif check == 1:
            if lastday < str(current.day):
                sendMessage(bot, query, 'Какие упражнения делали?')
                return EXERCISE
            else:
                sendMessage(bot, query, 'Отдохните, вы сегодня уже делали упражения)\nВаш пойнт: ' + str(point))
    elif option == 'expert':
        sendMessage(bot, query, 'Какие курсы вы проходите?')
        return EXPERT
    elif option == 'extra':
        sendMessage(bot, query, 'Какой челлендж?')
        return EXTRA
    elif option == 'reading':
        cursor.execute("SELECT * FROM Reading")
        arr = cursor.fetchall()
        check = -1
        lastday = ''
        for i in arr:
            if i[1] == chat_id:
                if i[3] == '*':
                    check = 0
                elif i[3] != '*':
                    lastday = str(i[3])[8:-19]
                    lasthour = str(i[3])[11:-16]
                    point = i[2]
                    check = 1
        if check == 0:
            sendMessage(bot, query, 'Какая книга?')
            return BOOK
        elif check == 1:
            if lastday < str(current.day) or (lastday == str(current.day) and str(int(lasthour)+4) <= str(current.hour)):
                sendMessage(bot, query, 'Какая книга?')
                return BOOK
            else:
                sendMessage(bot, query, 'Отдохните, вы недавно читали книгу)\nВаш пойнт: ' + str(point))

def askBook(bot, update):
    chat_id = update.message.chat_id
    book = update.message.text
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    all = cursor.fetchall()
    zone = ''
    point = 1
    for i in all:
        if i[0] == chat_id:
            zone = i[9]
    cursor.execute("SELECT * FROM Reading")
    arr = cursor.fetchall()
    for i in arr:
        if i[1] == chat_id:
            point = i[2]
    now_utc = datetime.datetime.now(pytz.timezone('UTC'))
    current = now_utc.astimezone(timezone(zone))
    cursor.execute("UPDATE Reading SET lastday = %s, point = %s, book = %s WHERE chat_id = %s",
                   [current, point * 2, book, chat_id])
    conn.commit()
    update.message.reply_text('Сколько страниц?')
    return PAGE

def askPage(bot, update):
    conn = psycopg2.connect("dbname=TimeTo user=postgres password=user")
    cursor = conn.cursor()
    chat_id = update.message.chat_id
    page = update.message.text
    if not page.isdigit():
        update.message.reply_text('Страница должна быть числом, попробуйте еще раз.')
        return PAGE
    cursor.execute("SELECT * FROM Reading")
    arr = cursor.fetchall()
    for i in arr:
        point = i[2]
    cursor.execute("UPDATE Reading SET page = %s WHERE chat_id = %s", [page, chat_id])
    conn.commit()
    update.message.reply_text('Круто! Ваш пойнт: ' + str(point))
    return ConversationHandler.END

def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    #Registration----------------------------------------------------------
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text, registration.askName)],
            BIRTH: [MessageHandler(Filters.text, registration.askBirth)],
            CITY: [MessageHandler(Filters.text, registration.askCity)],
            INSTA: [MessageHandler(Filters.text, registration.askInsta)],
            STUDY: [MessageHandler(Filters.text, registration.askStudy)],
            JOB: [MessageHandler(Filters.text, registration.askJob)],
            HOBBY: [MessageHandler(Filters.text, registration.askHobby)],
            GOALS: [MessageHandler(Filters.text, registration.askGoals)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)

    #Main Menu-------------------------------------------------------------
    dispatcher.add_handler(CommandHandler('cancel', cancel))
    dispatcher.add_handler(CommandHandler('gettop', leaderboard))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    m3 = ConversationHandler(
        entry_points=[CallbackQueryHandler(insight, pattern='m3')],
        states={
            INSIGHT: [MessageHandler(Filters.text, registration.askInsight)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(m3)
    dispatcher.add_handler(CallbackQueryHandler(statistics, pattern='m4'))
    dispatcher.add_handler(CallbackQueryHandler(profile, pattern='m5'))

    #Types-----------------------------------------------------------------
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='design'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='language'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='filmmaking'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='photography'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='finance'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='management'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='data science'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='web development'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='mobile development'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='dance'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='music'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='art'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='sport'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='oratory'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='stylist'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='startup'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='hardware'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='psychology'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='hiking'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='games'))
    dispatcher.add_handler(CallbackQueryHandler(registration.askType, pattern='travel'))
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='marketing'))
    #dispatcher.add_handler(CallbackQueryHandler(skills, pattern='others'))

    types = ConversationHandler(
        entry_points=[CallbackQueryHandler(registration.askType, pattern='send')],
        states={
            TIMEZONE: [MessageHandler(Filters.text, registration.askTimezone)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(types)

    #skills----------------------------------------------------------------
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='#design'))
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='#language'))
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='#filmmaking'))
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='#photography'))
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='#finance'))
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='#management'))
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='#data science'))
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='#web development'))
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='#mobile development'))
    dispatcher.add_handler(CallbackQueryHandler(skills, pattern='#marketing'))

    #challenges------------------------------------------------------------
    dispatcher.add_handler(CallbackQueryHandler(options, pattern='wakeup'))
    exc = ConversationHandler(
        entry_points=[CallbackQueryHandler(options, pattern='exercise')],
        states={
            EXERCISE: [MessageHandler(Filters.text, registration.askExercise)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(exc)
    exp = ConversationHandler(
        entry_points=[CallbackQueryHandler(options, pattern='expert')],
        states={
            EXPERT: [MessageHandler(Filters.text, registration.askExpert)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(exp)
    ext = ConversationHandler(
        entry_points=[CallbackQueryHandler(options, pattern='extra')],
        states={
            EXTRA: [MessageHandler(Filters.text, registration.askExtra)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(ext)
    read = ConversationHandler(
        entry_points=[CallbackQueryHandler(options, pattern='reading')],
        states={
            BOOK: [MessageHandler(Filters.text, askBook)],
            PAGE: [MessageHandler(Filters.text, askPage)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(read)
    dispatcher.add_handler(CallbackQueryHandler(options, pattern='scribing'))
    dispatcher.add_handler(CallbackQueryHandler(options, pattern='visualization'))
    updater.start_polling()
    updater.idle()

if (__name__ == '__main__'):
    main()

conn.close()

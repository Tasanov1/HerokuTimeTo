from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('#challenges', callback_data='m1')],
                #[InlineKeyboardButton('#skills', callback_data='m2')],
                [InlineKeyboardButton('#insight', callback_data='m3')],
                [InlineKeyboardButton('#statistics', callback_data='m4')],
                [InlineKeyboardButton('#profile', callback_data='m5')]]
    return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
    keyboard = [[InlineKeyboardButton('#wakeup', callback_data='wakeup')],
              [InlineKeyboardButton('#reading', callback_data='reading')],
              [InlineKeyboardButton('#exercise', callback_data='exercise')],
              [InlineKeyboardButton('#expert', callback_data='expert')],
              [InlineKeyboardButton('#scribing', callback_data='scribing')],
              [InlineKeyboardButton('#visualization', callback_data='visualization')],
              [InlineKeyboardButton('#extra', callback_data='extra')],
              [InlineKeyboardButton('Назад', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('#Design', callback_data='#design')],
                [InlineKeyboardButton('#WebDev', callback_data='#web development')],
                [InlineKeyboardButton('#Mobiledev', callback_data='#mobile development')],
                [InlineKeyboardButton('#DS', callback_data='#data science')],
                [InlineKeyboardButton('#Language', callback_data='#language')],
                [InlineKeyboardButton('#Filmmaking', callback_data='#filmmaking')],
                [InlineKeyboardButton('#Photography', callback_data='#photography')],
                [InlineKeyboardButton('#Marketing', callback_data='#marketing')],
                [InlineKeyboardButton('#Finance', callback_data='#finance')],
                [InlineKeyboardButton('#Management', callback_data='#management')],
                [InlineKeyboardButton('Назад', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

def choose_keyboard():
    keyboard = [[InlineKeyboardButton('design', callback_data='design')],
                [InlineKeyboardButton('web development', callback_data='web development')],
                [InlineKeyboardButton('mobile development', callback_data='mobile development')],
                [InlineKeyboardButton('data science', callback_data='data science')],
                [InlineKeyboardButton('language', callback_data='language')],
                [InlineKeyboardButton('filmmaking', callback_data='filmmaking')],
                [InlineKeyboardButton('photography', callback_data='photography')],
                [InlineKeyboardButton('marketing', callback_data='marketing')],
                [InlineKeyboardButton('finance', callback_data='finance')],
                [InlineKeyboardButton('management', callback_data='management')],

                [InlineKeyboardButton('dance', callback_data='dance')],
                [InlineKeyboardButton('music', callback_data='music')],
                [InlineKeyboardButton('art', callback_data='art')],
                [InlineKeyboardButton('sport', callback_data='sport')],
                [InlineKeyboardButton('oratory', callback_data='oratory')],
                [InlineKeyboardButton('stylist', callback_data='stylist')],
                [InlineKeyboardButton('startup', callback_data='startup')],
                [InlineKeyboardButton('hardware', callback_data='hardware')],
                [InlineKeyboardButton('psychology', callback_data='psychology')],
                [InlineKeyboardButton('hiking', callback_data='hiking')],
                [InlineKeyboardButton('games', callback_data='games')],
                [InlineKeyboardButton('travel', callback_data='travel')],
                #[InlineKeyboardButton('others', callback_data='others')],
                [InlineKeyboardButton('send', callback_data='send')]]
    return InlineKeyboardMarkup(keyboard)


"""
import datetime
import pytz
#print(str(datetime.datetime.now().astimezone()))
zone = pytz.all_timezones
input = '+06:00'
now_utc = datetime.datetime.now(pytz.timezone('UTC'))
zones = []
for i in zone:
    if input in str(now_utc.astimezone(pytz.timezone(i))):
        zones.append(i)

timezone = pytz.timezone('Antarctica/Vostok')
#print(now_utc.astimezone(timezone))
#print(len(pytz.all_timezones))
text1 = str(now_utc.astimezone(pytz.timezone('Asia/Almaty')))
text2 = now_utc.astimezone(pytz.timezone('Asia/Aqtau'))
print(text1[26:])
"""
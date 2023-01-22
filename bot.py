import telebot, json, time, schedule
from config import TOKEN, response_weather
from bd import connection, cursor, add_user, select_all_users
import emoji
from threading import Thread



bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    weather = telebot.types.KeyboardButton('Погода')
    markup.add(weather)
    info = (
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username,
        message.from_user.language_code,
    )
    print(info)
    print(message.chat.id)
    print(message.from_user.id)
    cursor.execute(f"SELECT EXISTS(SELECT personal_id from profilesio WHERE personal_id={message.from_user.id})")
    if cursor.fetchone()[0] == 0:
        cursor.execute(add_user, info)
        connection.commit()
        print('Пользователь добавлен!')
    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}! '
                                      f'Как дела?</b>', parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text.lower() == 'погода':
        info_weather = response_weather()
        temp = round((float(info_weather["Temperature"]) - 273.15), 2)
        feels_like = round((float(info_weather["Feels_like"]) - 273.15), 2)
        weather = emoji.emojize(f'( :alarm_clock: {info_weather["Date"]} :alarm_clock: ) \n В городе <b>'
                                f'{info_weather["City"]}</b> :snowflake:температура:fire: :'
                                f' <b>{temp}°C</b>, :snowflake:по ощущению:fire: : <b>{feels_like}°C</b>.')
        bot.send_message(message.chat.id, weather, parse_mode='html')
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'Вот твой ID: {message.from_user.id}')
    else:
        bot.send_message(message.chat.id, 'Я вас не понимать! ')

# @bot.message_handler(content_types=['photo'])
# def get_user_photo(message):
#     bot.send_message(message.chat.id, '<b>Вау, крутое фото! </b>', parse_mode='html')

#     bot.send_message(message.chat.id, text='Перейдите на сайт
# @bot.message_handler(commands=['website'])>
# def website(message):
#     markup = telebot.types.InlineKeyboardMarkup()
#     markup.add(telebot.types.InlineKeyboardButton('Посетить вебсайт', url='https://www.google.com'))
#     bot.send_message(message.chat.id, text='Перейдите на сайт.', reply_markup=markup)

# def text_for_every_day():
#     info_weather = response_weather()
#     temp = round((float(info_weather["Temperature"]) - 273.15), 2)
#     feels_like = round((float(info_weather["Feels_like"]) - 273.15), 2)
#     weather = emoji.emojize(f'( :alarm_clock: {info_weather["Date"]} :alarm_clock: ) \n В городе <b>'
#                             f'{info_weather["City"]}</b> :snowflake:температура:fire: :'
#                             f' <b>{temp}°C</b>, :snowflake:по ощущению:fire: : <b>{feels_like}°C</b>.')
#     bot.send_message(message.chat.id, weather, parse_mode='html')


def every():
    info_weather = response_weather()
    temp = round((float(info_weather["Temperature"]) - 273.15), 2)
    feels_like = round((float(info_weather["Feels_like"]) - 273.15), 2)
    weather = emoji.emojize(f'( :alarm_clock: {info_weather["Date"]} :alarm_clock: ) \n В городе <b>'
                            f'{info_weather["City"]}</b> :snowflake:температура:fire: :'
                            f' <b>{temp}°C</b>, :snowflake:по ощущению:fire: : <b>{feels_like}°C</b>.')
    info = cursor.execute(select_all_users)
    for i in info:
        bot.send_message(i[0], weather)

def send_message():
    schedule.every(6).hours.do(every)
    while True:
        schedule.run_pending()
        time.sleep(1)

thread = Thread(target=send_message, daemon=True)
thread.start()
bot.polling(non_stop=True)






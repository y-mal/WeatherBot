import telebot, json, time, schedule
from config import TOKEN, response_weather, CITY, TEXT_FOR_USERS
from bd import connection, cursor, add_user, select_all_personal_id_users, update_city
import emoji
from threading import Thread

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    weather = telebot.types.KeyboardButton('Погода')
    city_user = telebot.types.KeyboardButton('Указать свой город')
    markup.add(weather, city_user)
    info = (
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username,
        message.from_user.language_code,
    )
    cursor.execute(f"SELECT EXISTS(SELECT personal_id from profilesio WHERE personal_id={message.from_user.id})")
    if cursor.fetchone()[0] == 0:
        cursor.execute(add_user, info)
        connection.commit()
    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}! '
                                      f'Как дела?</b>', parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text.lower() == 'указать свой город':
        bot.send_message(message.chat.id, 'Введите цифру, чтобы указать свой город: \n'
                                          f'{TEXT_FOR_USERS}')
    if message.text in str(range(0, 10)):
        cursor.execute(update_city, [CITY[int(message.text)], message.from_user.id])
        connection.commit()
        bot.send_message(message.chat.id, f'Город <b>{CITY[int(message.text)]}</b> успешно обновлен! \n'
                                          f'Теперь вы будете получать рассылку погоды вашего города \n'
                                          f'каждые 6 часов !', parse_mode='html')
    if message.text.lower() == 'погода':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        for city in CITY:
            markup.add(telebot.types.KeyboardButton(city))
        bot.send_message(message.chat.id, 'Выберите свой город...', reply_markup=markup)
    if message.text in CITY:
        info_weather = response_weather(message.text)
        temp = round((float(info_weather["Temperature"]) - 273.15), 2)
        feels_like = round((float(info_weather["Feels_like"]) - 273.15), 2)
        weather = emoji.emojize(f'( :alarm_clock: {info_weather["Date"]} :alarm_clock: ) \n В городе <b>'
                                f'{info_weather["City"]}</b> :snowflake:температура:fire: :'
                                f' <b>{temp}°C</b>, :snowflake:по ощущению:fire: : <b>{feels_like}°C</b>.')
        bot.send_message(message.chat.id, weather, parse_mode='html')
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'Вот твой ID: {message.from_user.id}')

def every():
    weather_dict = {}
    for city in CITY:
        info_weather = response_weather(city)
        temp = round((float(info_weather["Temperature"]) - 273.15), 2)
        feels_like = round((float(info_weather["Feels_like"]) - 273.15), 2)
        weather = emoji.emojize(f'( :alarm_clock: {info_weather["Date"]} :alarm_clock: ) \n В городе <b>'
                                f'{info_weather["City"]}</b> :snowflake:температура:fire: :'
                                f' <b>{temp}°C</b>, :snowflake:по ощущению:fire: : <b>{feels_like}°C</b>.')
        weather_dict[city] = weather
    personal_id = cursor.execute(select_all_personal_id_users)
    for i in personal_id:
        if i[1] is not None:
            bot.send_message(i[0], weather_dict[i[1]], parse_mode='html')

def send_message():
    schedule.every(6).hours.do(every)
    while True:
        schedule.run_pending()
        time.sleep(1)

thread = Thread(target=send_message, daemon=True)
thread.start()
bot.polling(non_stop=True)




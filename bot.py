import telebot, json, time, schedule
from config import TOKEN, response_weather, CITY, TEXT_FOR_USERS
from bd import cursor, connection, add_user, select_all_personal_id_users, update_city, create_table_if_not_exists
import emoji
from threading import Thread
import logging  # Импортируем модуль логирования

# Настройка логирования в файл
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (можно менять на DEBUG для более подробных логов)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат вывода
    handlers=[
        logging.FileHandler("bot_logs.log"),  # Логи будут сохраняться в файле "bot_logs.log"
        logging.StreamHandler()  # Логи также будут выводиться в консоль
    ]
)
logger = logging.getLogger()  # Создаем объект логера

# Создание таблиц (если не существуют)
create_table_if_not_exists()

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
    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}! Как дела?</b>', parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    try:
        if message.text.lower() == 'указать свой город':
            bot.send_message(message.chat.id, 'Введите цифру, чтобы указать свой город: \n' f'{TEXT_FOR_USERS}')
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
    except Exception as e:
        logger.error(f"Error processing message from {message.from_user.id}: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка, попробуйте снова!")

def every():
    weather_dict = {}
    try:
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
    except Exception as e:
        logger.error(f"Error in weather update task: {e}")

def send_message():
    try:
        # Увеличиваем интервал между рассылками
        schedule.every(6).hours.do(every)  # Обновляем погоду каждые 6 часов
        # schedule.every(10).seconds.do(every)  # (опционально) Можно тестировать с более частыми интервалами

        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        logger.error(f"Error in scheduling task: {e}")

thread = Thread(target=send_message, daemon=True)
thread.start()

# Бот будет работать бесконечно, обрабатывая входящие сообщения
bot.polling(non_stop=True)

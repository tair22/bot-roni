#!/usr/bin/python

from config import token
import telebot
from telebot.util import extract_arguments
from random import choice
import requests

bot = telebot.TeleBot(token)

# Ключ API для OpenWeatherMap
WEATHER_API_KEY = "6dcc3c4ab4745739a518ab37e5d8021a"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

user_cars = {}

# Класс Car
class Car:
    def __init__(self, color, brand, model="Unknown", year=2023):
        self.color = color
        self.brand = brand
        self.model = model
        self.year = year
    
    def info(self):
        return f"🚗 {self.brand} {self.model} ({self.year})\n" \
               f"Цвет: {self.color}\n" \
               
               


@bot.message_handler(commands=['car'])
def car_handler(message):
    try:
        
        args_text = extract_arguments(message.text)
        
        if not args_text:
            bot.reply_to(message, "❌ Использование: /car <цвет> <марка> <модель> <год>\n\nПример: /car красный Toyota Highlander 2010")
            return
        
        
        args = args_text.split()
        
        if len(args) < 2:
            bot.reply_to(message, "❌ Укажите цвет и марку автомобиля\nПример: /car красный Toyota Highlander 2010")
            return
        
        color = args[0]
        brand = args[1]
        model = args[2] if len(args) > 2 else "Unknown"
        year = int(args[3]) if len(args) > 3 and args[3].isdigit() else 2023
        
        
        car = Car(color, brand, model, year)
        
        
        user_id = message.from_user.id
        if user_id not in user_cars:
            user_cars[user_id] = []
        
        user_cars[user_id].append(car)
        car_number = len(user_cars[user_id])
        
        
        bot.reply_to(message, f"✅ Создана новая машина (#{car_number})!\n\n{car.info()}\n\n/mycars - Посмотреть все созданные машины\n\n/carinfo <номер> - Информация о конкретной машине")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при создании автомобиля: {str(e)}")


@bot.message_handler(commands=['mycars'])
def mycars_handler(message):
    try:
        user_id = message.from_user.id
        
        if user_id not in user_cars or not user_cars[user_id]:
            bot.reply_to(message, "❌ У вас нет созданных машин. Используйте команду /car <цвет> <марка> <модель> <год>")
            return
        
        cars = user_cars[user_id]
        response = f"🚗 Ваши машины ({len(cars)} шт.):\n\n"
        
        for i, car in enumerate(cars, 1):
            response += f"#{i}. {car.info()}\n\n"
        
        bot.reply_to(message, response)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при получении списка машин: {str(e)}")


@bot.message_handler(commands=['carinfo'])
def carinfo_handler(message):
    try:
        user_id = message.from_user.id
        
        if user_id not in user_cars or not user_cars[user_id]:
            bot.reply_to(message, "❌ У вас нет созданных машин. Используйте команду /car <цвет> <марка> <модель> <год>")
            return
        
        args_text = extract_arguments(message.text)
        if not args_text or not args_text.isdigit():
            bot.reply_to(message, "❌ Использование: /carinfo <номер машины>\n\nПример: /carinfo 1")
            return
        
        car_number = int(args_text)
        cars = user_cars[user_id]
        
        if car_number < 1 or car_number > len(cars):
            bot.reply_to(message, f"❌ Машина #{car_number} не найдена. У вас есть машины с 1 по {len(cars)}")
            return
        
        car = cars[car_number - 1]
        bot.reply_to(message, f"🚗 Машина #{car_number}:\n\n{car.info()}")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

# Списки для различных команд
jokes_list = [
    "Почему программисты так плохо танцуют? У них нет алгоритма!",
    "Как называется утка-программист? Дак-типичный!",
    "Почему Python всегда мокрый? Потому что он в воде!",
    "Сколько программистов нужно, чтобы вкрутить лампочку? Ни одного, это hardware проблема!"
]

quotes_list = [
    "Код — это как юмор. Если вам приходится объяснять, то это плохой код. — Martin Fowler",
    "Преждевременная оптимизация — корень всех зол. — Donald Knuth",
    "Есть два способа создания дизайна программного обеспечения: один сделать его настолько простым, что в нем очевидно нет недостатков, и другой сделать его настолько сложным, что в нем нет очевидных недостатков. — C.A.R. Hoare",
    "Измеряй дважды, кодь один раз. — Народная мудрость программистов"
]

facts_list = [
    "Первый компьютерный баг был реальным насекомым — мотыльком, застрявшим в реле компьютера Harvard Mark II в 1947 году.",
    "Язык программирования Python назван не в честь змеи, а в честь британского комедийного шоу 'Monty Python's Flying Circus'.",
    "Пароль '123456' до сих пор остается одним из самых популярных паролей в мире.",
    "Первый в истории компьютерный вирус был создан в 1983 году и назывался 'Elk Cloner'."
]

def get_weather(city="Ufa"):
    """Получает данные о погоде для указанного города"""
    try:
        if WEATHER_API_KEY == "your_api_key_here" or not WEATHER_API_KEY:
            return "❌ API ключ не настроен. Получите ключ на https://openweathermap.org/api"
        
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        data = response.json()
        
        if data.get('cod') == 200:
            weather = data['weather'][0]['description'].capitalize()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            city_name = data['name']
            
            weather_icons = {
                'clear': '☀️', 'clouds': '☁️', 'rain': '🌧️', 'snow': '❄️',
                'thunderstorm': '⛈️', 'drizzle': '🌦️', 'mist': '🌫️'
            }
            
            icon = '🌤️'
            weather_main = data['weather'][0]['main'].lower()
            for key in weather_icons:
                if key in weather_main:
                    icon = weather_icons[key]
                    break
            
            return f"{icon} Погода в {city_name}:\n" \
                   f"• {weather}\n" \
                   f"• Температура: {temp}°C (ощущается как {feels_like}°C)\n" \
                   f"• Влажность: {humidity}%\n" \
                   f"• Ветер: {wind_speed} м/с"
        
        elif data.get('cod') == 401:
            return "❌ Неверный API ключ. Проверьте ключ на https://openweathermap.org/api"
        
        elif data.get('cod') == 404:
            return f"❌ Город '{city}' не найден. Проверьте название."
        
        else:
            return f"❌ Ошибка API: {data.get('message', 'Неизвестная ошибка')}"
            
    except requests.exceptions.Timeout:
        return "❌ Таймаут при запросе погоды. Попробуйте позже."
    except requests.exceptions.ConnectionError:
        return "❌ Ошибка подключения к серверу погоды."
    except Exception as e:
        return f"❌ Ошибка при получении погоды: {str(e)}"



@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
🚗 Добро пожаловать в бот с автомобилями!

📋 Доступные команды:

🚘 Команды автомобиля:
/car <цвет> <марка> <модель> <год> - Создать новую машину
/mycars - Посмотреть все созданные машины
/carinfo <номер> - Информация о конкретной машине

🎲 Развлекательные команды:
/joke - Случайная шутка
/quote - Мудрая цитата
/fact - Интересный факт
/weather [город] - Погода (по умолчанию: Уфа)
/coin - Подбросить монетку

📸 Также бот реагирует на фото, голосовые и файлы!
""")


@bot.message_handler(commands=['coin'])
def coin_handler(message):
    coin = choice(["ОРЕЛ", "РЕШКА"])
    bot.reply_to(message, f"🎲 {coin}")

@bot.message_handler(commands=['joke'])
def joke_handler(message):
    joke = choice(jokes_list)
    bot.reply_to(message, f"😂 {joke}")

@bot.message_handler(commands=['quote'])
def quote_handler(message):
    quote = choice(quotes_list)
    bot.reply_to(message, f"💡 {quote}")

@bot.message_handler(commands=['fact'])
def fact_handler(message):
    fact = choice(facts_list)
    bot.reply_to(message, f"📚 {fact}")

@bot.message_handler(commands=['weather'])
def weather_handler(message):
    try:
        parts = message.text.split()
        if len(parts) > 1:
            city = ' '.join(parts[1:])
        else:
            city = "Ufa"
            
        weather_report = get_weather(city)
        bot.reply_to(message, weather_report)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    bot.reply_to(message, "📸 Отличное фото! Спасибо, что поделились.")

@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    bot.reply_to(message, "🎤 Я получил ваше голосовое сообщение! К сожалению, я пока не умею их распознавать.")

@bot.message_handler(content_types=['document'])
def document_handler(message):
    filename = message.document.file_name if message.document.file_name else "файл"
    bot.reply_to(message, f"📄 Спасибо за файл: {filename}\nРазмер: {message.document.file_size} байт")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, f"🔁 {message.text}")

if __name__ == "__main__":
    bot.infinity_polling()
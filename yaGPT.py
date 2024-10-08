import os
import telebot
import requests
from telebot import types

# Получаем токен Telegram и API-ключ Yandex из переменных окружения
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
yandex_api_key = os.getenv('YANDEX_API_KEY')

# Проверяем, что токены получены
if telegram_token is None:
    print("Ошибка: Токен бота не установлен в переменной окружения.")
    exit(1)
if yandex_api_key is None:
    print("Ошибка: API-ключ Yandex не установлен в переменной окружения.")
    exit(1)

# Создаем экземпляр бота
bot = telebot.TeleBot(telegram_token)

# Функция запроса к Yandex GPT API
def yandex_gpt_request(user_input):
    prompt = {
        "modelUri": "gpt://b1g14jq77fnugn9t509v/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты ассистент дроид, способный помочь в галактических приключениях."
            },
            {
                "role": "user",
                "text": user_input  # Текст пользователя
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_api_key}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    if response.status_code == 200:
        return response.json()['result']['text']
    else:
        return "Ошибка при обращении к Yandex GPT API"

# Кнопка для запроса к Yandex GPT
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    key_gpt = types.InlineKeyboardButton(text='Запросить Yandex GPT', callback_data='gpt')
    keyboard.add(key_gpt)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'gpt':
        response = yandex_gpt_request("Привет! Мне нужна твоя помощь.")
        bot.send_message(call.message.chat.id, response)

# Обработка фотографий
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    response = yandex_gpt_analyze_image(downloaded_file)
    bot.send_message(message.chat.id, response)

# Функция анализа изображения с помощью Yandex GPT
def yandex_gpt_analyze_image(photo):
    return "Анализ изображения от Yandex GPT"

bot.polling(none_stop=True, interval=0)

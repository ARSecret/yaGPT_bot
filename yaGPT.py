import os
import telebot
import requests
from io import BytesIO

# Получаем токен Telegram, API-ключ Yandex и идентификатор каталога из переменных окружения
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
yandex_api_key = os.getenv('YANDEX_API_KEY')
folder_id = os.getenv('YANDEX_FOLDER_ID')

# Создаем экземпляр бота
bot = telebot.TeleBot(telegram_token)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "Приветствую! Я Яндекс помощник, чем могу помочь?"
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_reply_markup())

# Создание клавиатуры с кнопками
def create_reply_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("Ввести текст")
    btn2 = telebot.types.KeyboardButton("Обработка изображения")
    markup.add(btn1, btn2)
    return markup

# Обработка нажатия кнопки "Ввести текст"
@bot.message_handler(func=lambda message: message.text == "Ввести текст")
def handle_text_input(message):
    msg = bot.send_message(message.chat.id, "Введите текст для анализа:")
    bot.register_next_step_handler(msg, process_text)

def process_text(message):
    user_input = message.text
    response = yandex_gpt_request(user_input)
    bot.send_message(message.chat.id, response)

# Функция запроса к Yandex GPT API для текста
def yandex_gpt_request(user_input):
    prompt = {
        "modelUri": "gpt://b1g14jq77fnugn9t509v/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 2000
        },
        "messages": [
            {
                "role": "system",
                "text": "Привет, чем могу помочь?"
            },
            {
                "role": "user",
                "text": user_input
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_api_key}",
        "x-folder-id": folder_id
    }

    response = requests.post(url, headers=headers, json=prompt)

    if response.status_code == 200:
        result = response.json().get('result', {})
        text = result.get('alternatives', [{}])[0].get('message', {}).get('text', "Ошибка: ответ не содержит текста.")
        return text
    else:
        return f"Ошибка при обращении к Yandex GPT API: {response.status_code}"

# Обработка нажатия кнопки "Обработка изображения"
@bot.message_handler(func=lambda message: message.text == "Обработка изображения")
def handle_image_processing(message):
    bot.send_message(message.chat.id, "Высылайте фото для анализа.")

# Обработка фотографий
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Отправляем изображение на анализ
    response = yandex_gpt_analyze_image(downloaded_file)
    bot.send_message(message.chat.id, response)

# Функция анализа изображения с помощью Yandex GPT
def yandex_gpt_analyze_image(image_data):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {yandex_api_key}",
        "x-folder-id": folder_id
    }

    # Используем BytesIO для отправки изображения
    #files = {'file': ('image.jpg', BytesIO(image_data), 'image/jpeg')}
    #response = requests.post(url, headers=headers, files=files)

    #if response.status_code == 200:
    #    result = response.json().get('result', {})
    #    text = result.get('alternatives', [{}])[0].get('message', {}).get('text', "Ошибка: ответ не содержит текста.")
    #    return text
    #else:
    #    return f"Ошибка при обращении к Yandex GPT API: {response.status_code}"

# Запуск бота
bot.polling(none_stop=True, interval=0)

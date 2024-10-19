import os
import telebot
from yandex_gpt import yandex_gpt_request, yandex_gpt_analyze_image

# Получаем токен Telegram, API-ключ Yandex и идентификатор каталога из переменных окружения
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')

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

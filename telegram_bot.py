import os
import telebot
from yandex_gpt import yandex_gpt_request, yandex_ocr_analyze_image
from opencv import opencv_analyze_image

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
    btn2 = telebot.types.KeyboardButton("Обработка текста из изображения")
    btn3 = telebot.types.KeyboardButton("Распознавание изображения с OpenCV")
    markup.add(btn1, btn2, btn3)
    return markup


# Обработка нажатия кнопки "Ввести текст"
@bot.message_handler(func=lambda message: message.text == "Ввести текст")
def handle_text_input(message):
    msg = bot.send_message(message.chat.id, "Введите текст для анализа:")
    bot.register_next_step_handler(msg, process_text)


def process_text(message):
    user_input = message.text
    response = yandex_gpt_request(user_input)

    # Извлекаем текст из ответа Yandex GPT
    text = response.get('alternatives', [{}])[0].get('message', {}).get('text', "Ошибка: ответ не содержит текста.")

    # Отправляем результат пользователю
    bot.send_message(message.chat.id, text)


# Обработка нажатия кнопки "Обработка текста из изображения"
@bot.message_handler(func=lambda message: message.text == "Обработка текста из изображения")
def handle_image_processing(message):
    bot.send_message(message.chat.id, "Высылайте фото для анализа.")


# Обработка фотографий для OCR
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохраняем загруженный файл временно для анализа
    with open("temp_image.jpg", "wb") as temp_file:
        temp_file.write(downloaded_file)

    # Отправляем изображение на анализ с Yandex OCR
    response = yandex_ocr_analyze_image("temp_image.jpg")

    # Извлечение текста из результата OCR
    if 'results' in response:
        text_result = "\n".join([item['text'] for item in response['results']])
        bot.send_message(message.chat.id, f"Распознанный текст: {text_result}")
    else:
        bot.send_message(message.chat.id, "Ошибка: текст не был распознан.")


# Обработка нажатия кнопки "Распознавание изображения с OpenCV"
@bot.message_handler(func=lambda message: message.text == "Распознавание изображения с OpenCV")
def handle_opencv_processing(message):
    bot.send_message(message.chat.id, "Высылайте фото для распознавания.")


@bot.message_handler(content_types=['photo'])
def handle_opencv_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохраняем загруженный файл временно для анализа
    with open("temp_image.jpg", "wb") as temp_file:
        temp_file.write(downloaded_file)

    # Отправляем изображение на анализ с OpenCV
    response = opencv_analyze_image("temp_image.jpg")
    bot.send_message(message.chat.id, response)


# Запуск бота
bot.polling(none_stop=True, interval=0)

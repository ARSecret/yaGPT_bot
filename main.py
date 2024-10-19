import os
from telegram_bot import bot
from yandex_gpt import yandex_gpt_request, yandex_gpt_analyze_image

# Получаем токен Telegram, API-ключ Yandex и идентификатор каталога из переменных окружения
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
yandex_api_key = os.getenv('YANDEX_API_KEY')
folder_id = os.getenv('YANDEX_FOLDER_ID')

# Запуск бота
bot.polling(none_stop=True, interval=0)

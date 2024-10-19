from telegram_bot import bot
import os

if __name__ == "__main__":
    # Запуск бота
    bot.polling(none_stop=True, interval=0)

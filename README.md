# Telegram Bot with Yandex GPT Integration

## Установка

1. Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```

2. Установите переменные окружения:

    - Для Windows:
      ```bash
      set TELEGRAM_BOT_TOKEN=ваш_токен_бота
      set YANDEX_API_KEY=ваш_ключ_Yandex_API
      ```

    - Для Linux/MacOS:
      ```bash
      export TELEGRAM_BOT_TOKEN=ваш_токен_бота
      export YANDEX_API_KEY=ваш_ключ_Yandex_API
      ```

3. Запустите бота:
    ```bash
    python bot.py
    ```

## Функциональность

- Запрос к Yandex GPT через Telegram.
- Обработка фотографий.

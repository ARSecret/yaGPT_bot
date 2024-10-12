## Установка переменных окружения в PowerShell

Для корректной работы Telegram-бота с Yandex GPT API необходимо установить три переменные окружения: токен Telegram-бота, API-ключ Yandex и идентификатор каталога (folder-id). Для этого выполните следующие команды в PowerShell.

### Шаг 1. Установка переменных окружения

1. Откройте PowerShell и выполните команды:

```powershell
# Установить токен для Telegram
$env:TELEGRAM_BOT_TOKEN = "ваш_telegram_бот_токен"

# Установить API-ключ для Yandex
$env:YANDEX_API_KEY = "ваш_yandex_api_ключ"

# Установить идентификатор каталога (folder-id)
$env:YANDEX_FOLDER_ID = "ваш_yandex_folder_id"

# Проверить токен Telegram
$env:TELEGRAM_BOT_TOKEN

# Проверить API-ключ Yandex
$env:YANDEX_API_KEY

# Проверить идентификатор каталога
$env:YANDEX_FOLDER_ID

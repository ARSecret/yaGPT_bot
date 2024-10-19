import os
import requests

# Получаем токен Telegram, API-ключ Yandex и идентификатор каталога из переменных окружения
yandex_api_key = os.getenv('YANDEX_API_KEY')
folder_id = os.getenv('YANDEX_FOLDER_ID')

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

# Функция анализа изображения с помощью Yandex GPT
def yandex_gpt_analyze_image(image_data):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {yandex_api_key}",
        "x-folder-id": folder_id
    }

    # Используем BytesIO для отправки изображения
    # files = {'file': ('image.jpg', BytesIO(image_data), 'image/jpeg')}
    # response = requests.post(url, headers=headers, files=files)

    # if response.status_code == 200:
    #     result = response.json().get('result', {})
    #     text = result.get('alternatives', [{}])[0].get('message', {}).get('text', "Ошибка: ответ не содержит текста.")
    #     return text
    # else:
    #     return f"Ошибка при обращении к Yandex GPT API: {response.status_code}"

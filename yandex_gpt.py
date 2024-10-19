import os
import requests
import base64
import json
from mimetypes import guess_type

# Получаем токен Yandex и идентификатор каталога из переменных окружения
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

# Функция кодирования файла в Base64
def encode_file(file_path):
    with open(file_path, "rb") as fid:
        file_content = fid.read()
    return base64.b64encode(file_content).decode("utf-8")

# Функция анализа изображения с помощью Yandex OCR API
def yandex_ocr_analyze_image(file_path):
    mime_type, _ = guess_type(file_path)
    content = encode_file(file_path)

    data = {
        "mimeType": mime_type,
        "languageCodes": ["*"],
        "content": content
    }

    url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_api_key}",
        "x-folder-id": folder_id,
        "x-data-logging-enabled": "true"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return f"Ошибка при обращении к Yandex OCR API: {response.status_code}"


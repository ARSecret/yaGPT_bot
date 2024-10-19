import cv2

def opencv_analyze_image(image_path):
    # Загружаем изображение
    image = cv2.imread(image_path)
    if image is None:
        return "Ошибка: изображение не найдено или не удалось загрузить."

    # Загружаем заранее обученную модель для распознавания объектов
    model = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

    # Подготовка изображения для распознавания
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
    model.setInput(blob)

    # Выполнение распознавания
    detections = model.forward()

    # Обработка результатов распознавания
    objects_detected = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Порог уверенности
            objects_detected.append(f"Объект {i}: уверенность {confidence:.2f}")

    if not objects_detected:
        return "Объекты не распознаны."

    return "\n".join(objects_detected)

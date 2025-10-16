import cv2
from io import BytesIO
import numpy as np


def process_image(image_file):
    """
    Process the uploaded image to detect faces and return the image with rectangles drawn around detected faces.
    Args:
        image_file: An uploaded image file (e.g., from Flask's request.files).
    Returns:
        A tuple containing:
        - The processed image in bytes format.
        - The coordinates of the largest detected face as (x, y, w, h)
    """
    in_memory_file = BytesIO()
    image_file.save(in_memory_file)

    image_bytes = in_memory_file.getvalue()
    image_array = np.frombuffer(image_bytes, np.uint8)

    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

    if len(faces)== 0:
        return image_bytes, None
    
    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
    x, y, w, h = largest_face

    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    is_success, buffer = cv2.imencode(".jpg", image)

    return buffer.tobytes(), largest_face
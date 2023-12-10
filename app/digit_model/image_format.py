import os
from dataclasses import dataclass

import numpy as np
import keras
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.models import load_model


@dataclass
class RecognizePaths:
    model: keras.src.engine = load_model("app/digit_model/digit_recognition_model.keras")
    current_directory: str = os.path.dirname(__file__)
    file_path: str = os.path.join(current_directory, ".", "image", "resized_digit.png")


def recognize_digit(image_path: str) -> tuple[int, float]:
    img = Image.open(image_path)
    img = img.resize((28, 28))
    img = img.convert('P', palette=Image.ADAPTIVE, colors=256)

    img.save(RecognizePaths.file_path)

    img = img_to_array(img)
    img = img[np.newaxis, :, :, np.newaxis]

    result = RecognizePaths.model.predict([img])[0]
    recognized_digit = int(np.argmax(result))
    probability_of_recognized_digit = float(result[recognized_digit])

    return recognized_digit, probability_of_recognized_digit

import functools
import json
import numpy as np
import tensorflow as tf

from dataclasses import dataclass
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from backend.settings import RESOURCES_FOLDER


MODEL_BASE_FOLDER = RESOURCES_FOLDER / 'model_recognizer'


@dataclass
class VehicleModel:
    year: int
    name: str


def _preprocess_image(image_path: str, target_size: tuple[int, int]) -> np.ndarray:
    img = load_img(image_path, target_size=target_size)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)  # Expand dimensions to (1, height, width, channels)
    img /= 255.0  # Normalize pixel values
    return img


def _predict_vehicle_model(
    image_path: str,
    model: tf.keras.models.Model,
    class_indices: dict[int, str],
    target_size=(224, 224),
) -> str:
    img = _preprocess_image(image_path, target_size)
    probabilities = model.predict(img)
    predicted_class_index = np.argmax(probabilities)
    predicted_class = class_indices[predicted_class_index]
    return predicted_class


@functools.lru_cache
def _load_trained_model():
    return load_model(str(MODEL_BASE_FOLDER / 'model.h5'))


@functools.lru_cache
def _load_data_labels():
    with open(MODEL_BASE_FOLDER / 'labels.json', "r") as f:
        class_indices = json.load(f)
        index_to_class = {index: class_name for class_name, index in class_indices.items()}

    return index_to_class


def recognize_vehicle_model(image_path: str) -> VehicleModel | None:
    model = _load_trained_model()
    labels = _load_data_labels()

    predicted_class = _predict_vehicle_model(image_path, model, labels)

    if predicted_class is None:
        return None

    *model_name_parts, year = predicted_class.split(' ')

    return VehicleModel(name=' '.join(model_name_parts), year=int(year))

from functools import lru_cache

import cv2
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image

from backend import settings


@lru_cache
def _load_model():
    """ Load the MobileNetV2-SSDLite pre-trained model """
    print('Warming up MobileNetV2 model')
    return hub.load(str(settings.RESOURCES_FOLDER / 'ssd_mobilenet_v2_2'))


def _preprocess_image(image_path: str) -> tuple[tf.Tensor, Image]:
    """ Preprocess the input image """
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    input_tensor = tf.convert_to_tensor(image)
    input_tensor = input_tensor[tf.newaxis, ...]
    return input_tensor, image


def _get_vehicle_bounding_box(detections: dict, image: Image) -> list[int]:
    """ Get bounding box coordinates for the vehicle in the image """
    width, height = image.shape[1], image.shape[0]

    for i in range(int(detections['num_detections'])):
        class_id = int(detections['detection_classes'][0][i])
        score = detections['detection_scores'][0][i].numpy()

        # Check if the detected object is a vehicle (car, bus, or truck) and has a score higher than 0.5
        if class_id in [3, 6, 8] and score > 0.5:
            bbox = detections['detection_boxes'][0][i].numpy()
            ymin, xmin, ymax, xmax = bbox[0] * height, bbox[1] * width, bbox[2] * height, bbox[3] * width
            return [xmin, ymin, xmax, ymax]


def _crop_image_to_bounding_box(image: Image, bounding_box: list[int]):
    """ Crop the image to fit the vehicle """
    xmin, ymin, xmax, ymax = bounding_box
    cropped_image = image[int(ymin):int(ymax), int(xmin):int(xmax)]
    return cropped_image


def crop_vehicle_image(image_path: str) -> bool:
    model = _load_model()
    input_tensor, image = _preprocess_image(image_path)
    detections = model(input_tensor)
    bounding_box = _get_vehicle_bounding_box(detections, image)

    if bounding_box:
        cropped_image = _crop_image_to_bounding_box(image, bounding_box)
        cv2.imwrite(image_path, cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))
        return True

    return False

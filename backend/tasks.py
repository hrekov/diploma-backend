from celery import Celery

from backend import settings
from backend.logger import common_logger
from backend.services.colors import recognize_vehicle_color
from backend.services.cropping import crop_vehicle_photo
from backend.services.number_plates import recognize_number_plate
from backend.services.vehicle_model import recognize_vehicle_model_info


app = Celery('backend', broker=settings.CELERY_BROKER_URL)
app.conf.result_backend = settings.CELERY_RESULT_BACKEND_URL


@app.task
def schedule_photo_recognition(image_path: str) -> dict:
    crop_vehicle_photo(image_path)

    color = recognize_vehicle_color(image_path)

    try:
        number_plate = recognize_number_plate(image_path)
    except Exception:
        common_logger.exception('Unable to perform number plate recognition')
        number_plate = None

    try:
        vehicle_model_info = recognize_vehicle_model_info(image_path)
    except Exception:
        common_logger.exception('Unable to perform model info recognition')
        vehicle_model_info = None

    return {
        **(vehicle_model_info or {}),
        'number_plate': number_plate,
        'vehicle_color_hex': color,
        'vehicle_color_name': color,
    }

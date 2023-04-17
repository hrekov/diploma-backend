from pathlib import Path

from celery import Celery

from backend import settings
from backend.logger import common_logger
from backend.services.colors import recognize_vehicle_color
from backend.services.cropping import crop_vehicle_image
from backend.services.number_plates import recognize_number_plate
from backend.services.vehicle_model import recognize_vehicle_model_info


app = Celery('backend', broker=settings.CELERY_BROKER_URL)
app.conf.result_backend = settings.CELERY_RESULT_BACKEND_URL


@app.task
def schedule_photo_recognition(image_path: str) -> dict | None:
    is_cropped = crop_vehicle_image(image_path)

    if not is_cropped:
        print('Vehicle on image is not recognized')

        Path(image_path).unlink()  # Remove unneeded file

        return None

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

    result = {
        **(vehicle_model_info or {}),
        'number_plate': number_plate,
        'vehicle_color_hex': color,
        'vehicle_color_name': color,
    }

    # Remove unneeded file
    Path(image_path).unlink()

    return result

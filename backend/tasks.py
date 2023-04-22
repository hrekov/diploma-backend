from pathlib import Path
from celery import Celery

from backend import settings
from backend.logger import common_logger
from backend.services.colors import recognize_vehicle_color, hex_to_name
from backend.services.cropping import crop_vehicle_image
from backend.services.number_plates import recognize_number_plate
from backend.services.vehicle_model import recognize_vehicle_model
from backend.services.data_search import search_vehicle_in_knowledge_base


app = Celery('backend', broker=settings.CELERY_BROKER_URL)
app.conf.result_backend = settings.CELERY_RESULT_BACKEND_URL


@app.task
def schedule_photo_recognition(image_path: str) -> dict | None:
    is_cropped = crop_vehicle_image(image_path)

    if not is_cropped:
        print('Vehicle on image is not recognized')
        Path(image_path).unlink()
        return None

    results = dict()
    results['color_hex'] = recognize_vehicle_color(image_path)
    results['color_name'] = hex_to_name(results['color_hex'])

    try:
        results['number_plate'] = recognize_number_plate(image_path)
    except Exception:
        common_logger.exception('Unable to perform number plate recognition')
        results['number_plate'] = None

    try:
        vehicle_model = recognize_vehicle_model(image_path)
    except Exception:
        common_logger.exception('Unable to perform model info recognition')
        vehicle_model = None

    if vehicle_model is None:
        Path(image_path).unlink()
        return results

    results['year'] = vehicle_model.year

    if details := search_vehicle_in_knowledge_base(vehicle_model.name):
        results = {**details, **results}

    # Remove unneeded file
    Path(image_path).unlink()

    return results

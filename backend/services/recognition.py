import mimetypes
import typing
import uuid
import shutil
from pathlib import Path

from celery.result import AsyncResult

from backend.settings import MEDIA_PATH
from backend.tasks import schedule_photo_recognition


def _save_file_as_temporary(mime_type: str, file_contents: typing.BinaryIO) -> Path:
    extension = mimetypes.guess_extension(mime_type)

    assert extension is not None, f'Can not guess file extension for mime type {mime_type}'

    file_to_save_path = MEDIA_PATH / f'{uuid.uuid4()}{extension}'

    with open(file_to_save_path, 'wb') as file:
        shutil.copyfileobj(file_contents, file)

    return file_to_save_path


def recognize_vehicle_on_user_photo(mime_type: str, file_contents: typing.BinaryIO) -> AsyncResult:
    file_path = _save_file_as_temporary(mime_type, file_contents)

    return schedule_photo_recognition.delay(image_path=str(file_path))

import json

from celery.result import AsyncResult
from fastapi import APIRouter, UploadFile, HTTPException
from starlette.responses import StreamingResponse

from backend.services.recognition import recognize_vehicle_on_user_photo
from backend.tasks import schedule_photo_recognition, app as celery_app

router = APIRouter(prefix='/api/v1')


@router.post('/recognition')
def recognize_user_ui_uploaded_photo(photo: UploadFile) -> dict:
    if photo.content_type not in ('image/jpeg', 'image/png'):
        raise HTTPException(400, detail=f'File type of {photo.content_type} is not supported')

    scheduled_task = recognize_vehicle_on_user_photo(photo.content_type, photo.file)

    return {
        'task_id': scheduled_task.task_id,
    }


@router.get('/recognition/{task_id}')
def wait_for_task_result(task_id: str) -> StreamingResponse:
    def retrieve_task_result():
        task = AsyncResult(task_id, app=celery_app)
        result = task.get()

        yield json.dumps(result)

    return StreamingResponse(retrieve_task_result(), media_type='application/json')

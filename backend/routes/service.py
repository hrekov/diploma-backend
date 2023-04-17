from fastapi import APIRouter
from fastapi.responses import Response


router = APIRouter(prefix='/api/v1')


@router.get('/ping')
def ping() -> Response:
    return Response('pong', content_type='text/plain')

from fastapi import APIRouter

from . import service, recognition


router = APIRouter()
router.include_router(service.router)
router.include_router(recognition.router)

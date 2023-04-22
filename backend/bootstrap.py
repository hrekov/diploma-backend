from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import routes
from backend import signals


def build_application() -> FastAPI:
    app = FastAPI()

    app.include_router(routes.router)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=['*'],
        allow_methods=["*"],
    )

    app.on_event('startup')(signals.on_application_started)

    return app


app = build_application()

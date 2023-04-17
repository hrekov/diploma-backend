from fastapi import FastAPI

from backend import routes
from backend import signals


def build_application() -> FastAPI:
    app = FastAPI()

    app.include_router(routes.router)

    app.on_event('startup')(signals.on_application_started)

    return app


app = build_application()


import os

from django.core.asgi import get_asgi_application
from fastapi import FastAPI

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "web_simulation.settings"
)

django_app = get_asgi_application()

from .api import app as api_app

application = FastAPI(
    title="Simulation Jus de Fruit"
)

application.mount("/api", api_app)
application.mount("/", django_app)

app = application

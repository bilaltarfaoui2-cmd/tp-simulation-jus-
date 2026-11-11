# web_simulation/asgi.py
import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from api import api_app  # Kan-importiw l-API li qadina f Etape 2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_simulation.settings')
django_app = get_asgi_application()

app = FastAPI()

# Les requêtes li fihom /api kadihom l FastAPI
app.mount("/api", api_app)

# Les requêtes l-3adiyin kaymchiw l interface Django
app.mount("/", django_app)
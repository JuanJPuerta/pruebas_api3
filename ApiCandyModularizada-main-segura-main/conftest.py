# conftest.py
import os
import sys
import django

# Aseguramos que la carpeta apiCandySoft esté en sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "apiCandySoft"))

# Configuramos el settings de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apiCandySoft.settings")

django.setup()

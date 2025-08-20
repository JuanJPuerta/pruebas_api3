import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from servicio.models import Servicio
from servicio.views import ServicioViewSet

@pytest.mark.django_db
def test_crear_servicio():
    # Crear un servicio con datos mínimos válidos
    servicio = Servicio.objects.create(
        nombre='Manicure Básico',
        descripcion='Descripción sencilla',
        precio=20.00,
        tipo='Manicure'
    )
    assert servicio.pk is not None
    assert servicio.estado == 'Activo'  # Estado por defecto

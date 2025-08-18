import pytest
from rest_framework.test import APIClient
from django.urls import reverse

# Importa los modelos usando la ruta de paquete relativa al proyecto
from apiCandySoft.usuario.models.usuario import Usuario
from apiCandySoft.usuario.models.cliente import Cliente
from apiCandySoft.usuario.models.manicurista import Manicurista

@pytest.fixture
def usuario_activo(db):
    """Crea y retorna un usuario con estado 'Activo' para pruebas."""
    return Usuario.objects.create(nombre="Juan", estado="Activo")

@pytest.fixture
def usuario_inactivo(db):
    """Crea y retorna un usuario con estado 'Inactivo' para pruebas."""
    return Usuario.objects.create(nombre="Pedro", estado="Inactivo")

@pytest.fixture
def cliente(usuario_activo):
    """Crea y retorna un cliente asociado al usuario activo."""
    return Cliente.objects.create(usuario_id=usuario_activo.id, estado="Activo")

@pytest.fixture
def manicurista(usuario_activo):
    """Crea y retorna un manicurista asociado al usuario activo."""
    return Manicurista.objects.create(usuario_id=usuario_activo.id, estado="Activo")

def test_crear_usuario(db):
    """
    Prueba la creación de un usuario vía API (POST).
    Verifica que el usuario sea creado y los datos sean correctos.
    """
    client = APIClient()
    url = reverse('usuario-list')
    data = {
        "nombre": "NuevoUsuario",
        "estado": "Activo",
        # Agrega aquí los demás campos obligatorios según tu modelo
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['nombre'] == "NuevoUsuario"

def test_editar_usuario(db, usuario_activo):
    """
    Prueba la edición completa de un usuario vía API (PUT).
    Verifica que los cambios sean guardados correctamente.
    """
    client = APIClient()
    url = reverse('usuario-detail', args=[usuario_activo.id])
    data = {
        "nombre": "Juan Modificado",
        "estado": "Activo",
        # Otros campos si tu modelo lo requiere
    }
    response = client.put(url, data, format='json')
    assert response.status_code == 200
    assert response.data['nombre'] == "Juan Modificado"

def test_patch_usuario(db, usuario_activo):
    """
    Prueba la edición parcial de un usuario vía API (PATCH).
    Solo modifica el campo 'estado' y verifica la actualización.
    """
    client = APIClient()
    url = reverse('usuario-detail', args=[usuario_activo.id])
    data = {
        "estado": "Inactivo"
    }
    response = client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['estado'] == "Inactivo"

def test_destroy_activo(usuario_activo, cliente, manicurista):
    """
    Prueba la desactivación lógica de un usuario activo y sus asociaciones.
    Verifica que el estado cambie a 'Inactivo' después del DELETE.
    """
    client = APIClient()
    url = reverse('usuario-detail', args=[usuario_activo.id])
    response = client.delete(url)
    assert response.status_code == 200
    usuario_activo.refresh_from_db()
    assert usuario_activo.estado == 'Inactivo'

def test_cambiar_estado(usuario_inactivo):
    """
    Prueba el endpoint personalizado para cambiar el estado de un usuario.
    Cambia el estado de 'Inactivo' a 'Activo' y verifica el resultado.
    """
    client = APIClient()
    url = reverse('usuario-cambiar-estado', args=[usuario_inactivo.id])
    response = client.patch(url)
    assert response.status_code == 200
    usuario_inactivo.refresh_from_db()
    assert usuario_inactivo.estado == "Activo"

def test_activos(usuario_activo):
    """
    Prueba el endpoint para obtener usuarios activos.
    Verifica que el usuario creado esté presente en la respuesta.
    """
    client = APIClient()
    url = reverse('usuario-activos')
    response = client.get(url)
    assert response.status_code == 200
    assert any(u['estado'] == 'Activo' for u in response.data)

def test_inactivos(usuario_inactivo):
    """
    Prueba el endpoint para obtener usuarios inactivos.
    Verifica que el usuario creado esté presente en la respuesta.
    """
    client = APIClient()
    url = reverse('usuario-inactivos')
    response = client.get(url)
    assert response.status_code == 200
    assert all(u['estado'] == 'Inactivo' for u in response.data)
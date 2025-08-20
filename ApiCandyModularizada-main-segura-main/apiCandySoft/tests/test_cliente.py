import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from usuario.views.cliente import ClienteViewSet
from usuario.models.cliente import Cliente
from usuario.models.usuario import Usuario  # Importa el modelo Usuario también
from rol.models import Rol  # Importa el modelo Rol
from usuario.serializers.cliente import ClienteSerializer
from cita.models.cita_venta import CitaVenta
from cita.models.estado_cita import EstadoCita

#Primera Función
@pytest.mark.django_db
def test_cliente_create():
    # Crea un rol para asignar al usuario 
    rol_cliente = Rol.objects.create(
        # Asume que Rol tiene un campo 'nombre' o similar, ajusta según tu modelo Rol
        nombre="Cliente"
    )
    rol_manicurista = Rol.objects.create(
        nombre="Manicurista")

    # Crea el usuario pasando el rol creado en el campo rol_id
    usuario = Usuario.objects.create(
        username="testusuario",
        password="Testpassword1234",
        rol_id=rol_cliente  # clave foránea obligatoria
    )

    # Crea el cliente asociado a ese usuario
    cliente = Cliente.objects.create(
        usuario=usuario,
        nombre="Juan",
        apellido="Perez",
        tipo_documento="CC",
        numero_documento="1234567890",
        correo="testcorreo@gmail.com",
        celular="3001234567",
        estado="Activo"
    )


    assert cliente.nombre == "Juan"
    assert cliente.usuario.username == "testusuario"
    assert cliente.usuario.rol_id.nombre == "Cliente"

#Segunda función

@pytest.mark.django_db
def test_cliente_update():
    # Crear roles necesarios
    rol_cliente = Rol.objects.create(nombre="cliente")
    rol_otro = Rol.objects.create(nombre="otro_rol")

    # Crear usuario con rol inicial diferente a "cliente"
    usuario = Usuario.objects.create_user(
        username="testusuario",
        password="Testpassword1234",
        rol_id=rol_otro
    )

    # Crear cliente asociado
    cliente = Cliente.objects.create(
        usuario=usuario,
        nombre="Juan",
        apellido="Perez",
        tipo_documento="CC",
        numero_documento="1234567890",
        correo="testcorreo@gmail.com",
        celular="3001234567",
        estado="Activo"
    )

    # Datos para la actualización (validated_data)
    validated_data = {
        "username": "nuevo_usuario",
        "password": "NuevaPassword123",
        "nombre": "Juan Actualizado",
        "apellido": "Perez Actualizado",
        "correo": "nuevoemail@gmail.com"
    }

    # Instancia del serializer y llamar a update
    serializer = ClienteSerializer()
    cliente_actualizado = serializer.update(cliente, validated_data)

    # Validar cambios realizados
    assert cliente_actualizado.nombre == "Juan Actualizado"
    assert cliente_actualizado.apellido == "Perez Actualizado"
    assert cliente_actualizado.correo == "nuevoemail@gmail.com"
    assert cliente_actualizado.usuario.username == "nuevo_usuario"
    assert cliente_actualizado.usuario.rol_id.nombre == "cliente"
    assert cliente_actualizado.usuario.check_password("NuevaPassword123")

#Tercera función

@pytest.mark.django_db
def test_cambiar_estado():
    """
    Prueba la acción personalizada cambiar_estado que alterna el estado 
    Activo/Inactivo para cliente y usuario asociado.
    """

    rol_cliente = Rol.objects.create(nombre="cliente")
    usuario = Usuario.objects.create_user(
        username="user4",
        password="pass123",
        rol_id=rol_cliente,
        estado="Activo"
    )
    cliente = Cliente.objects.create(
        usuario=usuario,
        nombre="Test",
        apellido="User",
        tipo_documento="CC",
        numero_documento="126",
        correo="test4@test.com",
        estado="Activo"
    )

    factory = APIRequestFactory()
    request = factory.patch(f'/cliente/{cliente.usuario_id}/cambiar_estado/')
    force_authenticate(request, user=usuario)

    view = ClienteViewSet.as_view({'patch': 'cambiar_estado'})

    # Primera llamada alterna a Inactivo
    response = view(request, pk=cliente.usuario_id)
    assert response.status_code == 200
    cliente.refresh_from_db()
    usuario.refresh_from_db()
    assert cliente.estado == "Inactivo"
    assert usuario.estado == "Inactivo"

    # Segunda llamada alterna a Activo - reutilizamos la misma request
    response = view(request, pk=cliente.usuario_id)
    cliente.refresh_from_db()
    usuario.refresh_from_db()
    assert cliente.estado == "Activo"
    assert usuario.estado == "Activo"
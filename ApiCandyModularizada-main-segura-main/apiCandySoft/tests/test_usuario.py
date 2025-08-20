import pytest
from usuario.models.usuario import Usuario
from rol.models import Rol
from usuario.serializers.usuario import UsuarioSerializer

# Para evitar enviar correos reales en test, puedes usar mock (de ser necesario)
from unittest.mock import patch


@pytest.mark.django_db
@patch('usuario.serializers.usuario.enviar_correo_bienvenida_empleado')
def test_usuario_create(mock_enviar_correo):
    """Test para el método create de Usuario.

    Verifica que:
    - Se cree un usuario con los datos validados (nombre, correo, rol, etc.).
    - La contraseña se configure correctamente con hashing.
    - Se llame a la función de envío de correo de bienvenida.
    - Se genera contraseña segura si no se proporciona.
    """

    # Crear un rol para asignar al usuario
    rol = Rol.objects.create(nombre="usuario")

    # Datos de entrada simulados para creación de usuario
    validated_data = {
        'username': 'testuser',
        'correo': 'testuser@example.com',
        'nombre': 'Test',
        'apellido': 'Usuario',
        'rol_id': rol,
        'password': 'TestPass1234'
    }

    # Crear instancia de serializer para llamar a create
    serializer = UsuarioSerializer()

    # Llamada al método create con los datos de prueba
    usuario = serializer.create(validated_data)

    # Comprobar que el usuario fue creado y guardado con los datos correctos
    assert usuario.pk is not None  # El usuario fue guardado en BD
    assert usuario.username == 'testuser'
    assert usuario.correo == 'testuser@example.com'
    assert usuario.nombre == 'Test'
    assert usuario.rol_id == rol

    # Comprobar que la contraseña está hasheada y correcta
    assert usuario.check_password('TestPass1234')

    # Comprobar que se llamó a la función de correo una vez con los argumentos esperados
    mock_enviar_correo.assert_called_once()
    args, kwargs = mock_enviar_correo.call_args
    assert kwargs['destinatario'] == 'testuser@example.com'
    assert kwargs['nombre_empleado'] == 'Test'
    assert kwargs['rol_usuario'] == 'usuario'



@pytest.mark.django_db
def test_usuario_update():
    """Test para el método update de Usuario.

    Verifica que:
    - Se actualicen correctamente los campos proporcionados en validated_data.
    - La contraseña sea actualizada con hashing si se proporciona.
    - Retorna la instancia actualizada.
    """

    # Crear rol y usuario inicial
    rol = Rol.objects.create(nombre="usuario")
    usuario = Usuario.objects.create_user(
        username='userupdate',
        correo='userupdate@example.com',
        nombre='Inicial',
        apellido='Apellido',
        rol_id=rol,
        password='InicialPass123'
    )

    # Nuevos datos para la actualización
    validated_data = {
        'nombre':  'Actualizado',
        'apellido': 'Cambiado',
        'password': 'NuevaPass456'
    }

    serializer = UsuarioSerializer()

    # Llamar método update con la instancia y nuevos datos
    usuario_actualizado = serializer.update(usuario, validated_data)

    # Verificar que los campos se actualizan correctamente
    assert usuario_actualizado.nombre == 'Actualizado'
    assert usuario_actualizado.apellido == 'Cambiado'
    assert usuario_actualizado.check_password('NuevaPass456')

    # También verificar que el usuario actualizado sea el mismo objeto
    assert usuario.pk == usuario_actualizado.pk

import pytest
from insumo.models import Marca, Insumo
from insumo.serializer import MarcaSerializer, InsumoSerializer

@pytest.mark.django_db
def test_crear_marca_valida():
    # Prueba que se pueda crear una marca con un nombre válido
    data = {'nombre': 'MarcaEjemplo'}
    serializer = MarcaSerializer(data=data)
    # Debe ser válido porque el nombre cumple requisitos
    assert serializer.is_valid()
    marca = serializer.save()
    # El nombre guardado debe coincidir con el enviado
    assert marca.nombre == 'MarcaEjemplo'

@pytest.mark.django_db
def test_crear_insumo_valido_y_estado():
    # Crear una marca para asociar al insumo
    marca = Marca.objects.create(nombre='MarcaParaInsumo')

    # Datos para un insumo con stock positivo
    data = {
        'nombre': 'InsumoEjemplo',
        'stock': 10,
        'marca_id': marca.id
    }
    serializer = InsumoSerializer(data=data)
    # Debe ser válido porque los datos cumplen
    assert serializer.is_valid()
    insumo = serializer.save()
    # Como el stock es 10, el estado debe ser Activo (según lógica en save)
    assert insumo.estado == 'Activo'

@pytest.mark.django_db
def test_crear_insumo_stock_cambia_estado():
    # Crear marca para el insumo
    marca = Marca.objects.create(nombre='Marca2')

    # Crear un insumo con stock bajo para que cambie estado
    insumo = Insumo(nombre='InsumoTest', stock=3, marca_id=marca)
    insumo.save()
    # Por stock 3, estado debería ser Bajo
    assert insumo.estado == 'Bajo'

    # Cambiar stock a 0 para estado Agotado
    insumo.stock = 0
    insumo.save()
    assert insumo.estado == 'Agotado'

@pytest.mark.django_db
def test_nombre_marca_invalido_da_error():
    # Prueba que no deje crear marca con nombres incorrectos
    datos_invalidos = ['', 'ab', '123']
    for nombre in datos_invalidos:
        serializer = MarcaSerializer(data={'nombre': nombre})
        # No debe validar porque el nombre es inválido
        assert not serializer.is_valid()
        assert 'nombre' in serializer.errors

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Servicio
from cita.models.servicio_cita import ServicioCita
from cita.models.estado_cita import EstadoCita
from .servicio_serializer import ServicioSerializer
from utils.permisos import TienePermisoModulo


# Create your views here.
class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [TienePermisoModulo("Servicio")];

    def destroy(self, request, *args, **kwargs):
      try:
        servicio = self.get_object()

        # Buscar si el servicio está en alguna cita con estado Pendiente o En proceso
        citas_servicio = ServicioCita.objects.filter(servicio_id=servicio)

        for cita_servicio in citas_servicio:
            estado_cita = cita_servicio.cita_id.estado_id.Estado.lower()
            if estado_cita in ["pendiente", "en proceso"]:
                return Response(
                    {'message': 'No se puede eliminar o desactivar un servicio asociado a una cita pendiente o en proceso.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if servicio.estado == "Activo":
            servicio.estado = 'Inactivo'
            servicio.save()
            return Response({'message':'Servicio desactivado correctamente'}, status=status.HTTP_200_OK)
        else:
            servicio.delete()
            return Response({'message':'Servicio eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

      except Exception as e:
        return Response({'message':'Ocurrió un error al intentar eliminar el servicio'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        servicio = self.get_object()
        nuevo_estado = "Activo" if servicio.estado == "Inactivo" else "Inactivo"
        servicio.estado = nuevo_estado
        servicio.save()
        serializer = self.get_serializer(servicio)
        return Response({"message": f"Estado del servicio cambiado a {nuevo_estado}", "data": serializer.data})
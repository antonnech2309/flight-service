from django.shortcuts import render
from rest_framework import viewsets

from airport.models import Airport, AirplaneType, Airplane
from airport.serializers import AirportSerializer, AirplaneTypeSerializer, AirplaneSerializer, AirplaneListSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "list":
            serializer = AirplaneListSerializer

        return serializer

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Crew,
    Route,
    Order,
    Flight
)
from airport.serializers import (
    AirportSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    CrewSerializer,
    RouteSerializer,
    RouteListSerializer,
    OrderSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    OrderListSerializer,
    OrderDetailSerializer
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the airports with name"""
        name = self.request.query_params.get("name")

        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct()


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer

    def get_queryset(self):
        """Retrieve the airplanes with name"""
        name = self.request.query_params.get("name")

        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct()

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action in ("list", "retrieve"):
            serializer = AirplaneListSerializer

        return serializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def get_queryset(self):
        """Retrieve the crews with first_name and last_name"""
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        queryset = self.queryset

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset.distinct()


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action in ("list", "retrieve"):
            serializer = RouteListSerializer

        return serializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route__source",
        "tickets__flight__route__destination"
    )
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id)

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = OrderListSerializer

        if self.action == "retrieve":
            serializer = OrderDetailSerializer

        return serializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related(
        "route__source",
        "route__destination",
        "airplane"
    )
    serializer_class = FlightSerializer

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return serializer

from django.db import transaction
from rest_framework import serializers

from airport.models import Airport, AirplaneType, Airplane, Crew, Route, Order, Ticket, Flight


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(many=False, read_only=True)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = AirportSerializer(many=False, read_only=True)
    destination = AirportSerializer(many=False, read_only=True)


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew"
        )


class FlightListSerializer(serializers.ModelSerializer):
    flight_source = serializers.CharField(
        source="route.source.name",
        read_only=True
    )
    flight_destination = serializers.CharField(
        source="route.destination.name",
        read_only=True
    )
    flight_distance = serializers.IntegerField(
        source="route.distance",
        read_only=True
    )
    airplane_name = serializers.CharField(
        source="airplane.name",
        read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_source",
            "flight_destination",
            "flight_distance",
            "airplane_name",
            "departure_time",
            "arrival_time",
            "tickets_available"
        )


class TicketShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat")


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer(many=False, read_only=True)
    airplane = AirplaneListSerializer(many=False, read_only=True)
    crew = CrewSerializer(many=True, read_only=True)
    taken_seats = TicketShowSerializer(many=True, read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "taken_seats",
            "tickets_available"
        )


class FlightNameSerializer(FlightListSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_source",
            "flight_destination",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_seat(
            attrs["seat"],
            attrs["flight"].airplane.seats_in_row,
            attrs["row"],
            attrs["flight"].airplane.rows,
            serializers.ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketListSerializer(TicketSerializer):
    flight = FlightNameSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketDetailSerializer(TicketSerializer):
    flight = FlightListSerializer(many=False, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketDetailSerializer(many=True, read_only=True)

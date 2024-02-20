from rest_framework import serializers

from airport.models import Airport, AirplaneType, Airplane, Crew, Route, Order, Ticket, Flight


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ["id", "name", "closest_big_city"]


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ["id", "name"]


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats_in_row", "airplane_type"]


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = AirplaneTypeSerializer(many=False)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name"]


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]


class RouteListSerializer(RouteSerializer):
    source = AirportSerializer(many=False)
    destination = AirportSerializer(many=False)


# class TicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = ["id", "row", "seat", "flight"]
#
#
# class TicketListSerializer(TicketSerializer):
#     flight = FlightSerializer(many=False)


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["id", "route", "airplane", "departure_time", "arrival_time"]


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

    class Meta:
        model = Flight
        fields = [
            "id",
            "flight_source",
            "flight_destination",
            "flight_distance",
            "airplane_name",
            "departure_time",
            "arrival_time"
        ]


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer(many=False)
    airplane = AirplaneListSerializer(many=False)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "created_at"]

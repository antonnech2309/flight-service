from rest_framework import serializers

from airport.models import Airport, AirplaneType, Airplane


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

from airport.models import Airport, AirplaneType, Airplane, Crew, Route, Flight


def sample_airport(**params):
    defaults = {"name": "Boruspil", "closest_big_city": "Kyiv"}
    defaults.update(params)

    return Airport.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {"name": "private"}
    defaults.update(params)

    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()

    defaults = {
        "name": "Boeing",
        "rows": "12",
        "seats_in_row": "3",
        "airplane_type": airplane_type
    }
    defaults.update(params)

    return Airplane.objects.create(**defaults)


def sample_crew(**params):
    defaults = {
        "first_name": "Andrew",
        "last_name": "Pilotovs"
    }
    defaults.update(params)

    return Crew.objects.create(**defaults)


def sample_route(**params):
    source = sample_airport()
    destination = sample_airport(name="Zhylyanu")
    defaults = {
        "source": source,
        "destination": destination,
        "distance": 13
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()
    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": "2021-01-01 12:00:00",
        "arrival_time": "2021-01-01 14:00:00",
    }
    defaults.update(params)

    flight = Flight.objects.create(**defaults)
    flight.crew.add(sample_crew())

    return flight

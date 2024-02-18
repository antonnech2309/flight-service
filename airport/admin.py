from django.contrib import admin

from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Crew,
    Order,
    Route,
    Flight,
    Ticket
)

admin.register(Airport)
admin.register(AirplaneType)
admin.register(Airplane)
admin.register(Airport)
admin.register(Crew)
admin.register(Order)
admin.register(Route)
admin.register(Flight)
admin.register(Ticket)

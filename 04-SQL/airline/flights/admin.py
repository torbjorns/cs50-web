from django.contrib import admin

from .models import Flight, Airport, Passenger

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration") # creating a class to add these fields to the admin page

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin) # using the class
admin.site.register(Passenger, PassengerAdmin)
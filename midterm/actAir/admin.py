from django.contrib import admin

# Register your models here.

#Everything below here are my own code

from .models import * 

class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'gps')

class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('CO2', 'O3', 'NO2', 'PM10', 'PM2_5', 'DateTime', 'location')


admin.site.register(Location, LocationAdmin)

admin.site.register(Measurement, MeasurementAdmin)
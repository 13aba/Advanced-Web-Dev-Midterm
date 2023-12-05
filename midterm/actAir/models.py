from django.db import models

# Create your models here.

#Everything below this was writen by me

class Location(models.Model):
    location_name = models.CharField(max_length = 256, null=False, blank=False)
    gps = models.CharField(max_length = 256, null=False, blank=False)

    def __str__(self):
        return self.location_name
    


class Measurement(models.Model):
    CO2 = models.FloatField(null=False, blank=False)
    NO2 = models.FloatField(null=False, blank=False)
    O3 = models.FloatField(null=False, blank=False)
    PM10 = models.FloatField(null=False, blank=False)
    PM2_5 = models.FloatField(null=False, blank=False)
    DateTime = models.DateTimeField(null=False, blank=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


    def __str__(self):
        return self.DateTime.strftime("%d/%m/y %H")


#/air-quality/ Air quality - show every measurement will also accept data from user
#/location/ Location - show location informations
#/air-quality/{location}/ - show only that locations latest air measurements
#/air-quality/history/{location}?start_date={start}&end_date={end} - show locations air quality history depending on given date
#/air-quality/average/average?start_date={start}&end_date={end}  - show average air quality across all of the location
#/air-quality/element/{element}?start_date={start}&end_date={end} - show speficic elements history

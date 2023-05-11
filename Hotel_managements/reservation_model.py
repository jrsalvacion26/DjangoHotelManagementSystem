from Hotel_managements.models import Hotel
from django.db import models


class Reservation(models.Model):
    id_reservation = models.AutoField(primary_key=True)
    user = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reservations')
    user_update = models.CharField(max_length=100)
    room_type = models.CharField(max_length=100)
    Quantity = models.IntegerField()
    checkin_date = models.DateField()
    checkin_time = models.TimeField()
    
    class Meta:
        db_table = 'reservation'
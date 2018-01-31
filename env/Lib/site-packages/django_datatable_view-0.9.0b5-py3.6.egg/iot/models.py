from django.db import models


class IoT(models.Model):
    serial_no = models.CharField(max_length=50,unique=True,primary_key=True,blank=False)
    plate_no = models.CharField(max_length=50,blank=True)
    is_active = models.BooleanField(blank=False)

    def __str__(self):
        return self.serial_no
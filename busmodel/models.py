from django.db import models


class LudgersVehicle(models.Model):
    name = models.CharField(max_length=255)
    dummy_field_1 = models.IntegerField()
    dummy_field_2 = models.DateTimeField()
    dummy_field_3 = models.CharField(max_length=255)

    def __str__(self):
        return f"<Vehicle name=\"{self.name}\">"

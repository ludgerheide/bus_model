from django.db import models


class VehicleType(models.Model):
    """ Django model class representing a vehicle type

    Attributes:
    vehicle_type_id: [int] id for each type as primary key
    vehicle_type_name: [str] name of each type
    effective_capacity: [str] effective of battery capacity (kWh)
    opportunity_charging_possible: [bool] True for possible for opportunity charging
    effective_charging_curve: [str]
    effective_v2g_curve: [str]
    charging_efficiency: [float]
    minimal_charging_power: [float] in kW
    constant_evergy_consumption: [float] energy consumption when bus stops. can be 0
    vehicle_length: [float] in meters, for optimization of rotation plan
    """
    vehicle_type_id = models.IntegerField(primary_key=True)
    vehicle_type_name = models.CharField(max_length=255)
    effective_capacity = models.FloatField()
    opportunity_charging_possible = models.BooleanField()
    effective_charging_curve = models.CharField(max_length=255)
    effective_v2g_curve = models.CharField(max_length=255)
    charging_efficiency = models.FloatField()
    minimal_charging_power = models.FloatField()
    constant_evergy_consumption = models.FloatField()
    vehicle_length = models.FloatField()

    def __str__(self):
        """for test only"""
        return f'{self.vehicle_type_name}, {self.vehicle_name}'

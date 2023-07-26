"""
    Definition of
"""
from django.db import models
import numpy as np
import math


class ChargingCurve(models.Model):
    """ Django model class representing charging curve
    According to Abb. 5.5 in Enrico's dissertation and simplified

    Attributes:

    vehicle_type [str]
    soc_min: [float]
    soc_th: [float] threshold state of charge, where the charging curve changes from CC to CV
    soc_max: [float]
    p_cc: [float] constant charging power in kW


    """
    vehicle_type = models.CharField(max_length=255)  # is it necessary?
    soc_min = models.FloatField()
    soc_th = models.FloatField()
    soc_max = models.FloatField()
    p_cc = models.FloatField()


class VehicleClass(models.Model):
    """ Django model representing an upper-class of a vehicle

    Attributes:
    vehicle_class_id: [int] primary key
    vehicle_class_name: [str]
    """

    vehicle_class_id = models.IntegerField(primary_key=True)
    vehicle_class_name = models.CharField(max_length=255)


class VehicleType(models.Model):
    """ Django model representing a vehicle type

    Attributes:
    vehicle_type_id: [int] primary key
    vehicle_type_name: [str] name of each type
    effective_capacity: [str] effective of battery capacity (kWh)
    opportunity_charging_possible: [bool] True for possible for opportunity charging
    effective_charging_curve: [str]
    effective_v2g_curve: [str]
    charging_efficiency: [float]
    minimal_charging_power: [float] in kW
    constant_evergy_consumption: [float] energy consumption when bus stops. can be 0
    vehicle_length: [float] in meters, for optimization of rotation plan
    vehicle_class: [VehicleClass]
    """
    vehicle_type_id = models.IntegerField(primary_key=True)
    vehicle_type_name = models.CharField(max_length=255)
    effective_capacity = models.FloatField()
    opportunity_charging_possible = models.BooleanField()
    effective_charging_curve = models.ForeignKey(ChargingCurve, on_delete=models.CASCADE)
    effective_v2g_curve = models.JSONField()  # placeholder for now
    charging_efficiency = models.FloatField()
    minimal_charging_power = models.FloatField()
    constant_energy_consumption = models.FloatField()
    vehicle_length = models.FloatField()
    vehicle_class = models.ForeignKey(VehicleClass, on_delete=models.CASCADE)

    def charging_curve(self):
        """
        :return: pre-computed charging curve
        A simplified charging curve of Enrico's (5.3), with charging power constant before soc_th and exponentially
        decrease with time after reaching soc_th
        """

        soc_min = self.effective_charging_curve.soc_min
        soc_max = self.effective_charging_curve.soc_max
        soc_th = self.effective_charging_curve.soc_th
        p_eff = self.effective_charging_curve.p_cc * self.charging_efficiency
        e_eff = self.effective_capacity

        t = np.linspace(0, math.ceil(e_eff * (soc_max - soc_min) / p_eff), num=21)
        soc = []

        t_th = (soc_th - soc_min) * e_eff / p_eff

        for tau in t:
            if tau <= t_th:
                soc_tp = p_eff * tau / e_eff + soc_min
            else:
                soc_tp = p_eff * math.exp(t_th) * (math.exp(-t_th) - math.exp(-tau)) / e_eff + soc_th

            if soc_tp > soc_max:
                soc_tp = soc_max

            soc.append(soc_tp)

        return t, soc

    def interpolation(self, t):
        """
            will return an soc value by interpolation
        """
        return np.interp(t, self.charging_curve)

    def __str__(self):
        """print id and name"""
        return f'{self.vehicle_type_id}, {self.vehicle_type_name}'


class Rotation(models.Model):
    """Django model for rotation

    rotation_id: [int] primary key
    rotation_name: [str]
    vehicle_class: [VehicleClass] assign an appropriate vehicle class to each rotation
    opportunity_charging_possible: [bool]
    """
    rotation_id = models.IntegerField(primary_key=True)
    rotation_name = models.FloatField(max_length=255)
    vehicle_class = models.ForeignKey(VehicleClass, on_delete=models.CASCADE)
    opportunity_charging_possible = models.BooleanField()


class Trip(models.Model):
    """Trip

    trip_id: [int] primary key
    rotation_id: [Rotation] the rotation this trip belongs to
    departure_station
    arrival_station
    departure_time
    arrival_time
    distance:
    temperature
    incline
    speed
    """
    trip_id = models.IntegerField(primary_key=True)
    rotation_id = models.ForeignKey(Rotation, on_delete=models.CASCADE)
    departure_station = models.CharField(max_length=255)  # placeholder, might be foreign key of station table
    arrival_station = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    distance = models.FloatField()
    temperature = models.FloatField()
    incline = models.FloatField()
    speed = models.FloatField()

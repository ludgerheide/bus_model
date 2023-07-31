"""
    Definition of
"""
from django.db import models
import numpy as np
import math


class ChargingCurve(models.Model):
    """ Django model class representing charging curve
    According to Abb. 5.5 and equation 5.3 in the dissertation of E. Lauth

    Attributes:

    vehicle_type [str]
    soc_min: [float]
    soc_th: [float] threshold state of charge, where the charging curve changes from CC to CV
    soc_max: [float]
    p_cc: [float] constant charging power in kW
    energy_nominal: [float]

   """
    vehicle_type = models.CharField(max_length=255)  # is it necessary?
    soc_min = models.FloatField()
    soc_th = models.FloatField()
    soc_max = models.FloatField()
    p_cc = models.FloatField()
    energy_nominal = models.FloatField()

    def get_exponential_power(self, soc):
        """get spontaneous charging power with exponential charging curve.
        Source: eflips.depot.processes.exponential_power() by E.Lauth"""

        if soc < self.soc_th:
            return self.p_cc
        else:
            return self.p_cc / 10 * (1 / self.energy_nominal - 10) / (math.exp(1) - math.exp(self.soc_th)) * (
                    math.exp(soc) - math.exp(self.soc_th)) + self.p_cc


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

    def charging_curve(self, precision=0.1):
        """
        :return: pre-computed charging curve, linear estimation of equation (5.3) in the dissertation of E.Lauth
        Source: eflips.depot.processes.ChargeEquationSteps.estimate_duration() by E.Lauth
        """

        soc_min = self.effective_charging_curve.soc_min
        soc_max = self.effective_charging_curve.soc_max
        e_eff = self.effective_capacity

        soc = soc_min
        dur = 0
        soc_list = [soc_min, ]
        time_list = [dur, ]
        while soc < soc_max:
            soc_interval = float(min(precision, soc_max - soc))
            soc += soc_interval
            soc_list.append(soc)
            amount = e_eff * soc_interval

            power = self.effective_charging_curve.get_exponential_power(soc)
            effective_power = power * self.charging_efficiency
            dur += amount / effective_power
            time_list.append(dur)

        return time_list, soc_list

    def interpolation(self, t, precision=0.1):
        """
            will return an soc value by interpolation
        """
        time_list, soc_list = self.charging_curve(precision)
        return np.interp(t, time_list, soc_list, left=self.effective_charging_curve.soc_min,
                         right=self.effective_charging_curve.soc_max)

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
    departure_station: [str]
    arrival_station: [str]
    departure_time: [DateTimeField]
    arrival_time: [DateTimeField]
    distance: [float]
    temperature: [float]
    incline: [float]
    speed: [float]
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


from django.test import TestCase

from busmodel.models import VehicleType


class VehicleTestClass(TestCase):
    def setUp(self):
        """Test of successful objects creation"""
        VehicleType.objects.create(vehicle_type_id="1", vehicle_type_name="SB", effective_capacity="300.0",
                                   opportunity_charging_possible="True", effective_charging_curve="0.1, 0.2",
                                   effective_v2g_curve="0.3, 0.4", charging_efficiency="0.5",
                                   minimal_charging_power="30.5", constant_evergy_consumption="10.2",
                                   vehicle_length="8.7")

        VehicleType.objects.create(vehicle_type_id="2", vehicle_type_name="AB", effective_capacity="250.0",
                                   opportunity_charging_possible="False", effective_charging_curve="0.3, 0.3",
                                   effective_v2g_curve="0.4, 0.4", charging_efficiency="0.45",
                                   minimal_charging_power="35.5", constant_evergy_consumption="15.4",
                                   vehicle_length="14.3")

    def test_vehicles(self):
        """Test of successful query and attribute interpretation"""
        sb = VehicleType.objects.get(vehicle_type_name="SB")
        ab = VehicleType.objects.get(vehicle_type_name="AB")

        def test_vehicle_model(bus):
            self.assertIsInstance(bus.vehicle_type_id, int)
            self.assertIsInstance(bus.vehicle_type_name, str)
            self.assertIsInstance(bus.effective_capacity, float)
            self.assertIsInstance(bus.opportunity_charging_possible, bool)
            self.assertIsInstance(bus.effective_charging_curve, str)
            self.assertIsInstance(bus.effective_v2g_curve, str)
            self.assertIsInstance(bus.charging_efficiency, float)
            self.assertIsInstance(bus.minimal_charging_power, float)
            self.assertIsInstance(bus.constant_evergy_consumption, float)
            self.assertIsInstance(bus.vehicle_length, float)

        test_vehicle_model(sb)
        test_vehicle_model(ab)

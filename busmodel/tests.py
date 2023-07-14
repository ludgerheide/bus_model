import datetime

from django.test import TestCase

from busmodel.models import Vehicle


class VehicleTestCase(TestCase):
    def setUp(self):
        now = datetime.datetime.now()
        now_no_tz = datetime.datetime.now().replace(tzinfo=None)
        Vehicle.objects.create(name="lion", dummy_field_1=1, dummy_field_2=now, dummy_field_3="3")
        Vehicle.objects.create(name="cat", dummy_field_1=1, dummy_field_2=now_no_tz, dummy_field_3="3")

    def test_vehicles(self):
        """Animals that can speak are correctly identified"""
        lion = Vehicle.objects.get(name="lion")
        cat = Vehicle.objects.get(name="cat")

        self.assertIsInstance(lion.dummy_field_1, int)
        self.assertIsInstance(cat.dummy_field_1, int)

        self.assertIsInstance(lion.dummy_field_2, datetime.datetime)
        self.assertIsInstance(cat.dummy_field_2, datetime.datetime)

        self.assertIsInstance(lion.dummy_field_3, str)
        self.assertIsInstance(cat.dummy_field_3, str)

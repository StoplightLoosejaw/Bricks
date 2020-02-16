from django.test import TestCase
from ..models import House, Brick_Task


class HouseTest(TestCase):
    """ Test module for House model """

    def setUp(self):
        House.objects.create(
            address='Москва, Ленинградское шоссе д.7', total_bricks_required=1000)
        House.objects.create(
            address='Оренбург, Зеленая улица д.4', total_bricks_required=400)

    def test_house_bricks(self):
        house_1 = House.objects.get(pk=1)
        house_2 = House.objects.get(address='Оренбург, Зеленая улица д.4')
        self.assertEqual(
            house_1.get_bricks(), "Москва, Ленинградское шоссе д.7 requires 1000 bricks. Now there are 0 bricks ")
        self.assertEqual(
            house_2.get_bricks(), "Оренбург, Зеленая улица д.4 requires 400 bricks. Now there are 0 bricks ")


class BrickTaskTest(TestCase):
    """ Test module for Brick_Task model """

    def setUp(self):
        House.objects.create(
            address='Москва, Ленинградское шоссе д.7', total_bricks_required=1000)

        Brick_Task.objects.create(
            house_id=House.objects.get(pk=1), bricks=5, date_load="2023-02-10")
        
    def test_house_bricks(self):
        brick_task = Brick_Task.objects.get(house_id=1)
        self.assertEqual(
            brick_task.get_bricks() + ' to '
            + brick_task.house_id.address, "5 bricks dispatch 2023-02-10 to Москва, Ленинградское шоссе д.7")

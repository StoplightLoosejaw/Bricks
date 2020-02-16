from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date
from ..models import House
from ..serializers import HouseSerializer


class HouseTest(APITestCase):
    def test_post_building(self):
        """
        Ensure we can create a new building.
        """
        url = '/building/'
        data = {"address": "дом 50 улица Ленина", "total_bricks_required": 300}
        today = date.today()
        date_output = today.strftime("%Y-%m-%d")
        data_output = {
                        "id": 1,
                        "address": "дом 50 улица Ленина",
                        "date_start": date_output,
                        "date_completed": None,
                        "date_last_load": None,
                        "bricks_at_the_moment": 0,
                        "total_bricks_required": 300,
                        "date_updated": date_output
                        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data_output)


class BrickTaskTest(APITestCase):

    def setUp(self):
        House.objects.create(
            address='Москва, Ленинградское шоссе д.7', total_bricks_required=1000)
        House.objects.create(
            address='Оренбург, Зеленая улица д.4', total_bricks_required=400)
        
    def test_post_brick_task(self):
        """
        Ensure that without a building we can not create a new brick_task.
        """
        task_url = '/building/id/3/add-bricks'
        task_data = {
            "bricks": 200,
            "date_load": "2030-03-10"
            }
        response = self.client.post(task_url, task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': "There is no such house!"})

        """
        Ensure that with a building we can create a new brick_task.
        """
        
        task_url = '/building/id/1/add-bricks'
        response = self.client.post(task_url, task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_output = {
                        "id": 1,
                        "bricks": 200,
                        "date_load": "2030-03-10",
                        "excessive_bricks": 0,
                        "house_id": 1
                     }
                        
        self.assertEqual(response.data, data_output)

        today = date.today()
        date_output = today.strftime("%Y-%m-%d")
        house = House.objects.get(pk=1)
        house_output = {
                        "id": 1,
                        "address": "Москва, Ленинградское шоссе д.7",
                        "date_start": date_output,
                        "date_completed": None,
                        "date_last_load": "2030-03-10",
                        "bricks_at_the_moment": 200,
                        "total_bricks_required": 1000,
                        "date_updated": date_output
                        }
        serializer = HouseSerializer(house)
        self.assertEqual(serializer.data, house_output)

        """
        Ensure that you can create dispath task that takes place before the last one.
        """

        task_url = '/building/id/1/add-bricks'
        task_data = {
            "bricks": 50,
            "date_load": "2025-03-10"
            }
        response = self.client.post(task_url, task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        today = date.today()
        date_output = today.strftime("%Y-%m-%d")
        data_output = {
                        "id": 2,
                        "bricks": 50,
                        "date_load": "2025-03-10",
                        "excessive_bricks": 0,
                        "house_id": 1
                     }
                        
        self.assertEqual(response.data, data_output)

        house = House.objects.get(pk=1)
        house_output = {
                        "id": 1,
                        "address": "Москва, Ленинградское шоссе д.7",
                        "date_start": date_output,
                        "date_completed": None,
                        "date_last_load": "2030-03-10",
                        "bricks_at_the_moment": 250,
                        "total_bricks_required": 1000,
                        "date_updated": date_output
                        }
        serializer = HouseSerializer(house)
        self.assertEqual(serializer.data, house_output)

        """
        Ensure that when there are more bricks than required to complete building they go to excessive.
        """

        task_url = '/building/id/1/add-bricks'
        task_data = {
            "bricks": 1000,
            "date_load": "2030-03-10"
            }
        response = self.client.post(task_url, task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        today = date.today()
        date_output = today.strftime("%Y-%m-%d")
        data_output = {
                        "id": 3,
                        "bricks": 750,
                        "date_load": "2030-03-10",
                        "excessive_bricks": 250,
                        "house_id": 1
                     }
                        
        self.assertEqual(response.data, data_output)

        house = House.objects.get(pk=1)
        house_output = {
                        "id": 1,
                        "address": "Москва, Ленинградское шоссе д.7",
                        "date_start": date_output,
                        "date_completed": "2030-03-10",
                        "date_last_load": "2030-03-10",
                        "bricks_at_the_moment": 1000,
                        "total_bricks_required": 1000,
                        "date_updated": date_output
                        }
        serializer = HouseSerializer(house)
        self.assertEqual(serializer.data, house_output)

        """
        Ensure that when building is complete you cant dispatch bricks to it.
        """

        response = self.client.post(task_url, task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': "House is already completed, no more bricks required"})

        self.assertEqual(serializer.data, house_output)

        """
        Ensure that you cant dispatch bricks back in time.
        """

        task_url = '/building/id/2/add-bricks'
        task_data = {
            "bricks": 250,
            "date_load": "1980-03-10"
            }
        response = self.client.post(task_url, task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': "You can't lay bricks before construction starts"})

        self.assertEqual(serializer.data, house_output)


class StatsTest(APITestCase):

    def setUp(self):
        House.objects.create(
            address='Москва, Ленинградское шоссе д.7', total_bricks_required=1000)
        House.objects.create(
            address='Оренбург, Зеленая улица д.4', total_bricks_required=400)

    def test_post_brick_task(self):
        """
        Dispatch some bricks and check the stats
        """
        
        task_url = '/building/id/1/add-bricks'
        task_data = {
            "bricks": 100,
            "date_load": "2030-03-10"
            }
        self.client.post(task_url, task_data, format='json')

        task_url = '/building/id/1/add-bricks'
        task_data = {
            "bricks": 200,
            "date_load": "2031-03-10"
            }
        self.client.post(task_url, task_data, format='json')

        task_url = '/building/id/1/add-bricks'
        task_data = {
            "bricks": 100,
            "date_load": "2031-03-10"
            }
        self.client.post(task_url, task_data, format='json')
        
        task_url = '/building/id/1/add-bricks'
        task_data = {
            "bricks": 400,
            "date_load": "2032-03-10"
            }
        self.client.post(task_url, task_data, format='json')

        task_url = '/building/id/2/add-bricks'
        task_data = {
            "bricks": 400,
            "date_load": "2032-03-10"
            }
        self.client.post(task_url, task_data, format='json')

        stats_url = '/stats'
        stats_output = [
                        {
                            "house_id__address": "Москва, Ленинградское шоссе д.7",
                            "date_load": "2030-03-10",
                            "bricks_sum": 100
                        },
                        {
                            "house_id__address": "Москва, Ленинградское шоссе д.7",
                            "date_load": "2031-03-10",
                            "bricks_sum": 400
                        },
                        {
                            "house_id__address": "Москва, Ленинградское шоссе д.7",
                            "date_load": "2032-03-10",
                            "bricks_sum": 800
                        },
                        {
                            "house_id__address": "Оренбург, Зеленая улица д.4",
                            "date_load": "2032-03-10",
                            "bricks_sum": 400
                        },
                        ]
                            
        response = self.client.get(stats_url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, stats_output)

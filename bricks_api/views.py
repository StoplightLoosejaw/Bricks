from rest_framework.decorators import api_view
from .models import House, Brick_Task
from rest_framework.response import Response
from rest_framework import status
from .serializers import HouseSerializer, BrickTaskSerializer, HouseBricksSerializer
from django.db.models import Sum, Window, F
from datetime import datetime


# Create your views here.'

@api_view(['POST', 'GET'])
def new_building(request):
    if request.method == 'GET':
        houses = House.objects.all()
        serializer = HouseSerializer(houses, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = {
            'address': request.data.get('address'),
            'total_bricks_required': request.data.get('total_bricks_required'),
        }
        serializer = HouseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def new_task(request, pk):
    try:
        house = House.objects.get(pk=pk)
    except House.DoesNotExist:
        return Response({'message': "There is no such house!"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        tasks = Brick_Task.objects.all()
        serializer = BrickTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        task_data = {
            'bricks': request.data.get('bricks'),
            'house_id': pk,
            'date_load': request.data.get('date_load'),
            'excessive_bricks': 0
        
        }
        if house.date_start > datetime.strptime(task_data['date_load'], "%Y-%m-%d").date():
            return Response({'message': "You can't lay bricks before construction starts"},
                            status=status.HTTP_400_BAD_REQUEST)
        if house.date_completed:
            return Response({'message': "House is already completed, no more bricks required"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            if house.date_last_load:
                if house.date_last_load > datetime.strptime(task_data['date_load'], "%Y-%m-%d").date():
                    pass
            else:
                house.date_last_load = task_data['date_load']
            if house.bricks_at_the_moment + request.data.get('bricks') > house.total_bricks_required:
                task_data['excessive_bricks'] = abs(house.total_bricks_required -
                                                    (house.bricks_at_the_moment + request.data.get('bricks')))
                task_data['bricks'] -= task_data['excessive_bricks']
                house.bricks_at_the_moment = house.total_bricks_required
                house.date_completed = house.date_last_load
            else:
                house.bricks_at_the_moment += request.data.get('bricks')
        serializer = BrickTaskSerializer(data=task_data)
        if serializer.is_valid():
            house.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_stats(request):
    if request.method == 'GET':
        houses = Brick_Task.objects.select_related().\
            values('house_id__address', 'bricks', 'date_load').\
            annotate(bricks_sum=Window(Sum('bricks'), partition_by='house_id__address', order_by=F('date_load').asc()))\
            .values('house_id__address', 'date_load', 'bricks_sum').distinct().order_by()
        serializer = HouseBricksSerializer(houses, many=True)
        return Response(serializer.data)

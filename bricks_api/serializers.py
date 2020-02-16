from .models import House, Brick_Task
from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class BrickTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brick_Task
        fields = '__all__'


class HouseBricksSerializer(serializers.ModelSerializer):
    bricks_sum = serializers.IntegerField()
    house_id__address = serializers.CharField()

    class Meta:
        model = Brick_Task
        fields = ('house_id__address', 'date_load', 'bricks_sum')

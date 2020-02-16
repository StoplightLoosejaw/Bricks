from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class House(models.Model):
    address = models.CharField(max_length=255, unique=True)
    date_start = models.DateField(auto_now_add=True)
    date_completed = models.DateField(null=True, blank=True, default=None)
    date_last_load = models.DateField(null=True, blank=True, default=None)
    bricks_at_the_moment = models.IntegerField(default=0)
    total_bricks_required = models.IntegerField(validators=[MinValueValidator(1)])
    date_updated = models.DateField(auto_now=True)

    def get_bricks(self):
        return self.address + ' requires ' + str(self.total_bricks_required) + \
               ' bricks. Now there are ' + str(self.bricks_at_the_moment) + ' bricks '


class Brick_Task(models.Model):
    bricks = models.IntegerField(validators=[MinValueValidator(1)])
    house_id = models.ForeignKey(House, related_name='brick_tasks', on_delete=models.CASCADE)
    date_load = models.DateField()
    excessive_bricks = models.IntegerField(default=0)

    def get_bricks(self):
        return str(self.bricks) + ' bricks dispatch ' + str(self.date_load)

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Place(models.Model):
  name = models.CharField(max_length = 255)
  address = models.CharField(max_length = 255)
  tag = models.IntegerField(validators=[MaxValueValidator(3)]) # 0: food, 1: drink, 2: party
  neighborhood = models.CharField(max_length = 255)
  instagram = models.CharField(max_length=255)
  open_time = models.TimeField(auto_now=False, auto_now_add=False)
  close_time = models.TimeField(auto_now=False, auto_now_add=False)
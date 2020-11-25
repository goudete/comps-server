from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Place(models.Model):
  name = models.CharField(max_length = 255)
  address = models.CharField(max_length = 255)
  tag = models.IntegerField(validators=[MaxValueValidator(3)]) # 0: food, 1: drink, 2: party
  neighborhood = models.CharField(max_length = 255)
  instagram = models.CharField(max_length=255)
  open_time = models.TimeField(auto_now=False, auto_now_add=False)
  close_time = models.TimeField(auto_now=False, auto_now_add=False)

class Ratings(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  place = models.ForeignKey(Place, on_delete=models.CASCADE)
  rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
  if created:
    Token.objects.create(user=instance)
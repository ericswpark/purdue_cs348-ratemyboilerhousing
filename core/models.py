from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Housing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)
    address = models.TextField(max_length=150)

class RoomType(models.Model):
    id = models.AutoField(primary_key=True)
    friendly_name = models.TextField(max_length=20)
    bedroom_count = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    bathroom_count = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])

class Offering(models.Model):
    id = models.AutoField(primary_key=True)
    housing = models.ForeignKey(Housing, related_name="offerings", on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, related_name="offerings", on_delete=models.CASCADE)
    cost = models.IntegerField(default=0, help_text="Cost of offering in cents (for example, $500 is 50,000)")

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    offering = models.ForeignKey(Offering, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name="reviews", on_delete=models.CASCADE)

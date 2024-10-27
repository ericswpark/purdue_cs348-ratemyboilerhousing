from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Housing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50)
    address = models.TextField(max_length=150)

    def __str__(self):
        return self.name

class RoomType(models.Model):
    id = models.AutoField(primary_key=True)
    friendly_name = models.TextField(max_length=20)
    bedroom_count = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    bathroom_count = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.friendly_name} - ({self.bedroom_count}BD {self.bathroom_count}BA)"

class Offering(models.Model):
    id = models.AutoField(primary_key=True)
    housing = models.ForeignKey(Housing, related_name="offerings", on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, related_name="offerings", on_delete=models.CASCADE)
    cost = models.IntegerField(default=0, help_text="Cost of offering in cents (for example, $500 is 50,000)")

    def get_formatted_cost(self):
        return f"${self.cost / 100}"

    def get_review_count(self):
        return self.reviews.count()

    def __str__(self):
        return f"{self.housing} - {self.room_type} - {self.get_formatted_cost()}"

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    offering = models.ForeignKey(Offering, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name="reviews", on_delete=models.CASCADE)
    stars = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)], help_text="Number of stars in half star increments (for example, 5 stars is 10, while 2 and a half stars is 5)")
    description = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s review on {self.offering} ({self.created_at})"
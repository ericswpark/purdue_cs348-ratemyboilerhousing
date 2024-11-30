from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Min, Max, Avg

User = get_user_model()


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

    def has_reviews(self):
        return self.get_review_count() > 0

    def __str__(self):
        return f"{self.housing} - {self.room_type} - {self.get_formatted_cost()}"

    @classmethod
    def get_min_cost(cls):
        return cls.objects.aggregate(Min("cost"))["cost__min"]

    @classmethod
    def get_max_cost(cls):
        return cls.objects.aggregate(Max("cost"))["cost__max"]

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    offering = models.ForeignKey(Offering, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    stars = models.IntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)], help_text="Number of stars in half star increments (for example, 5 stars is 10, while 2 and a half stars is 5)")
    description = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s review on {self.offering.housing} - {self.offering.room_type} - {self.created_at.strftime("%B %d, %Y")}"

    def get_normalized_star_count(self):
        return self.stars / 2

class Statistics(models.Model):
    date = models.DateField(auto_now_add=True, primary_key=True)

    generated_at = models.DateTimeField(auto_now_add=True)

    user_count = models.IntegerField(default=0)
    housing_count = models.IntegerField(default=0)
    offering_count = models.IntegerField(default=0)
    review_count = models.IntegerField(default=0)

    offering_cost_avg = models.FloatField(default=0)
    offering_cost_min = models.IntegerField(default=0)
    offering_cost_max = models.IntegerField(default=0)

    review_stars_avg = models.FloatField(default=0)
    review_stars_min = models.IntegerField(default=0)
    review_stars_max = models.IntegerField(default=0)

    @classmethod
    def get_today_stats(cls):
        if cls.objects.filter(date=datetime.today()).exists():
            return cls.objects.get(date=datetime.today())

        # Today's statistics not found, generate one!
        stat = cls.objects.create(
            date=datetime.today(),
            generated_at=datetime.now(),
            user_count=User.objects.all().count(),
            housing_count=Housing.objects.all().count(),
            review_count=Review.objects.all().count(),
            offering_cost_avg=Offering.objects.aggregate(Avg("cost"))["cost__avg"],
            offering_cost_min=Offering.get_min_cost(),
            offering_cost_max=Offering.get_max_cost(),
            review_stars_avg=Review.objects.aggregate(Avg("stars"))["stars__avg"],
            review_stars_min=Review.objects.aggregate(Min("stars"))["stars__min"],
            review_stars_max=Review.objects.aggregate(Max("stars"))["stars__max"]
        )
        stat.save()
        return stat

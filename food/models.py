from django.db import models
from django.contrib.auth.models import User

class FoodLog(models.Model):

    MEAL_TYPE_CHOICES=[
        ('breakfast','breakfast'),
        ('lunch','lunch'),
        ('dinner','dinner'),
        ('snacks','snacks')
    ]

    title=models.CharField(max_length=200)
    calories=models.IntegerField()
    meal_type=models.CharField(max_length=200,choices=MEAL_TYPE_CHOICES)
    serving_size=models.CharField(max_length=200)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.title}"
    
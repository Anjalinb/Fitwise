from rest_framework import serializers

from django.contrib.auth.models import User

from food.models import FoodLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]

class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=FoodLog
        fields="__all__"
        read_only_fields=["id","created_at","owner"]
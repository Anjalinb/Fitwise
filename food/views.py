from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from food.serializers import UserSerializer,FoodLogSerializer
from food.models import FoodLog
from food.permissions import IsOwner
from food.ai_service import get_diet_plan

from datetime import datetime

class SignUpView(APIView):

    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializer(data=form_data)

        if serializer_instance.is_valid():
            cleaned_data=serializer_instance.validated_data
            user_obj=User.objects.create_user(**cleaned_data)
            serializer_instance=UserSerializer(user_obj)
            return Response(data=serializer_instance.data)

        else:
            return Response(data=serializer_instance.errors)

class GetMeView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        auth_user=request.user
        instance=User.objects.get(username=auth_user)
        serializer_instance=UserSerializer(instance)
        return Response(data=serializer_instance.data)

class FoodListCreateView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        qs=FoodLog.objects.filter(owner=request.user)
        serializer_instance=FoodLogSerializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=FoodLogSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(owner=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)


class FoodLogRetrieveUpdateDeleteView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[IsOwner]

    def get(self,request,pk=None):
        instance=get_object_or_404(FoodLog,id=pk)
        self.check_object_permissions(request,instance)
        serialzer_instance=FoodLogSerializer(instance)
        return Response(data=serialzer_instance.data)

    def put(self,request,pk=None):
        form_data=request.data
        instance=get_object_or_404(FoodLog,id=pk)
        self.check_object_permissions(request,instance)
        serializer_instance=FoodLogSerializer(data=form_data,instance=instance)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk=None):
        instance=get_object_or_404(FoodLog,id=pk)
        self.check_object_permissions(request,instance)
        instance.delete()
        return Response(data={"message":"deleted"})


class CalorieSummaryView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        response_data={
            "todays_total":0
        }

        cur_date=datetime.now().date()
        cur_month=datetime.now().month
        cur_year=datetime.now().year

        todays_calories=FoodLog.objects.filter(owner=request.user,created_at__date=cur_date)
        monthly_calories=FoodLog.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_calories:
            monthly_total=monthly_calories.values("calories").aggregate(total_calories=Sum("calories")).get("total_calories")
            monthly_summary=monthly_calories.values("meal_type").annotate(total_calories=Sum("calories"))
            response_data["monthly_total"]=monthly_total
            response_data["monthly_summary"]=monthly_summary


        if todays_calories:
            todays_total=todays_calories.values("calories").aggregate(total_calories=Sum("calories")).get("total_calories")
            meal_type_summary=todays_calories.values("meal_type").annotate(total_calories=Sum("calories"))

            response_data["todays_total"]=todays_total
            response_data["meal_type_summary"]=meal_type_summary

        return Response(data=response_data)

class DietPlanView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        response_data={
            "monthly_total":0
        }

        cur_month=datetime.now().month
        cur_year=datetime.now().year

        monthly_calories=FoodLog.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_calories:
            monthly_total=monthly_calories.values("calories").aggregate(total=Sum("calories")).get("total")
            monthly_summary=monthly_calories.values("meal_type").annotate(total=Sum("calories"))
            response_data["monthly_total"]=monthly_total
            response_data["monthly_summary"]=monthly_summary
            diet_plan=get_diet_plan(response_data)
            response_data["plan"]=diet_plan

        return Response(data=response_data)





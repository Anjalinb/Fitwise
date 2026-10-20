from django.urls import path

from food.views import SignUpView,GetMeView,FoodListCreateView,FoodLogRetrieveUpdateDeleteView,CalorieSummaryView
from food.views import DietPlanView

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns=[
    path('signup/',SignUpView.as_view()),
    path('getme/',GetMeView.as_view()),
    path('foodlog/',FoodListCreateView.as_view()),
    path('foodlog/<int:pk>/',FoodLogRetrieveUpdateDeleteView.as_view()),
    path('foodlog/summary/',CalorieSummaryView.as_view()),
    path('foodlog/dietplan/',DietPlanView.as_view()),
    path('token/',ObtainAuthToken.as_view()),
]
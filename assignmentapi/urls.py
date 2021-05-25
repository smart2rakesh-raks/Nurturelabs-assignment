from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from advisor import views
from django.contrib import admin

urlpatterns = [
    path('user/register/', views.User_register.as_view()),
    path('user/login/', views.User_login.as_view()),
    path('admin/advisor/', views.Advisor_View.as_view()),
    path('user/<user_id>/advisor/', views.Advisor_list_View.as_view()),
    path('user/<user_id>/advisor/<advisor_id>/', views.Booking_View.as_view()),
    path('user/<user_id>/advisor/booking/', views.Booking_View.as_view()),
]
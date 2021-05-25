from rest_framework import serializers
from rest_framework.serializers import Serializer, ImageField, EmailField, DateTimeField
from .models import User, Advisor, Booking
from datetime import datetime



class AdvisorSerializer(serializers.HyperlinkedModelSerializer):
    photo = ImageField()
    class Meta:
        model = Advisor
        fields = ['id', 'name', 'photo']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField()
    USERNAME_FIELD = 'email'

    def validate_email(self, value):
        l_email = value.lower()
        if User.objects.filter(email__iexact=l_email).exists():
            return serializers.ValidationError("Email already exists")
        return l_email

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

class BookingSerializer(serializers.ModelSerializer):
    booking_time = DateTimeField()
    advisor = serializers.PrimaryKeyRelatedField(queryset=Advisor.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Booking
        fields = ['id', 'booking_time', 'advisor', 'user']

from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, Advisor, Booking
from advisor.serializers import AdvisorSerializer, UserSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

class User_register(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        request_data = request.data
        user_serializer = UserSerializer(data=request_data)
        user_serializer.is_valid()
        user = user_serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
           "token": str(refresh.access_token),
           "user_id": user.id
        }
        return Response(res)

class User_login(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            res = {
                "token": str(refresh.access_token),
                "user_id": user.id
            }
            return Response(res)
        else:
            return Response([], status=status.HTTP_401_UNAUTHORIZED)



class Advisor_View(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvisorSerializer
    queryset = Advisor.objects.all()

    def post(self,request):
        file_serializer = AdvisorSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response([], status=status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Advisor_list_View(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AdvisorSerializer
    queryset = Advisor.objects.all()

    def get(self,user_id, request, *args, **kwargs, ):
        user_id = self.kwargs['user_id']
        advisors = Advisor.objects.filter(id =user_id)
        return Response(advisors)


class Booking_View(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get(self,user_id, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        res = []
        user = User.objects.get(id=user_id)
        if user is not None:
            bookings = user.bookings.all()
            for booking in bookings:
                advisor = AdvisorSerializer(booking.advisor)
                booking_time = booking.booking_time.strftime("%d/%m/%Y %H:%M:%S")
                res = {
                    'id': booking.id,
                    'booking_time': booking_time,
                    'advisor': advisor.data
                }
                res.append(res)
        return Response(res)

    def post(self,user_id, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        advisor_id = self.kwargs.get('advisor_id')
        booking_time = request.data.get('booking_time')
        Data = {
                'user': user_id,
                'advisor': advisor_id,
                'booking_time': booking_time,
            }
        booking_serializer = BookingSerializer(data=Data)
        if booking_serializer.check_booking_time_available(advisor_id, booking_time):
            if booking_serializer.is_valid():
                booking_serializer = booking_serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(booking_serializer.errors)

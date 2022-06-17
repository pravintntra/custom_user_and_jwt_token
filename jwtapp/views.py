from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from jwtapp.models import User
from jwtapp.serializers import (
    UserSerializers,
    EmployeeSerializers,
    MyTokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    AUTH_HEADER_TYPES,
    InvalidToken,
    TokenError,
)
from rest_framework import generics, status

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import time

# Create your views here.


class Dashboard(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user_obj = User.objects.all()
        serializer = UserSerializers(user_obj, many=True)
        channel_layer = get_channel_layer()
        # for item in range(1, 10):
        # data = {"count":item}
        async_to_sync(channel_layer.group_send)(
            "new_test_room_group", {"type": "send_new_notification", "value": serializer.data}
        )
            # time.sleep(1)
        return Response(
            {
                "users": serializer.data,
                "status": True,
                "message": "Successfully get all users data",
            },
            status.HTTP_200_OK,
        )


class MyTokenObtainPairView(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = MyTokenObtainPairSerializer

    www_authenticate_realm = "api"

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .permissions import IsSelf
from rooms.serializers import RoomSerializer
from rooms.models import Room


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["POST"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, permission_classes=IsAuthenticated)
    def me(self, request):
        return Response(UserSerializer(request.user).data)

    @me.mapping.put
    def modify_me(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    @favs.mapping.put
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()
        if pk:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)

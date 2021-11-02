from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Room


class RoomSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer()

    class Meta:
        model = Room
        # fields = "__all__"
        fields = ("name", "price", "instant_book", "user")

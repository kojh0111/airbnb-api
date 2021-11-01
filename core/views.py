from django.core import serializers
from django.http import HttpResponse
from rooms.models import Room


# Create your views here.
def list_rooms(request):
    rooms = Room.objects.all()
    data = serializers.serialize("json", rooms)
    response = HttpResponse(data)
    return response

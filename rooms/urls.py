from django.urls import path
from . import views

urlpatterns = [
    path("", views.RoomsView.as_view()),
    path("search/", views.room_search),
    path("<int:pk>/", views.RoomView.as_view()),
]

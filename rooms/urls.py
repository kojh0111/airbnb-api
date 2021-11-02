from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register("", viewsets.RoomViewset, basename="room")

urlpatterns = router.urls

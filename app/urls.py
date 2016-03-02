from django.conf.urls import url, include

from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register(r'photos', viewsets.PhotoViewSet, 'photos')

urlpatterns = [
	url(r'^', include(router.urls))
]

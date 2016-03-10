from django.conf.urls import url, include

from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register(r'photos', viewsets.PhotoViewSet, 'photos')
router.register(r'effects', viewsets.EffectViewSet, 'effects')

urlpatterns = [
	url(r'^', include(router.urls))
]

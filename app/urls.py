from django.conf.urls import url, include

from rest_framework import routers

from . import viewsets
from . import views

router = routers.DefaultRouter()
router.register(r'photos', viewsets.PhotoViewSet, 'photos')
router.register(r'effects', viewsets.EffectViewSet, 'effects')

urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^loginstatus', views.is_logged_in, name='loginstatus')
]

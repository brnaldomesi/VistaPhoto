from django.conf.urls import url, include

from rest_framework import routers

from . import viewsets
from . import views

router = routers.DefaultRouter()
router.register(r'photos', viewsets.PhotoViewSet, 'photos')
router.register(r'effects', viewsets.EffectViewSet, 'effects')
router.register(r'edit', viewsets.PhotoEditViewSet, 'edit')

urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^login/status/', views.is_logged_in, name='loginstatus')
]

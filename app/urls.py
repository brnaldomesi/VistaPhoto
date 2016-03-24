from django.conf.urls import url, include

from rest_framework import routers

from . import viewsets
from . import views

router = routers.DefaultRouter()
router.register(r'photo', viewsets.PhotoViewSet, 'photo')
router.register(r'preview', viewsets.PreviewViewSet, 'preview')
router.register(r'edit', viewsets.PhotoEditViewSet, 'edit')

urlpatterns = [
	url(r'^', include(router.urls)),
    url(r'^login/status/', views.is_logged_in, name='loginstatus')
]

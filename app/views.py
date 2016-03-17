from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
def index(request):
	"""Display the login template."""
	return render(request, 'views/angular_base.html', {'request': request})

@api_view(['GET'])
def is_logged_in(request):
    """Method view to check if request is coming from a user who is logged in
    through a Django backends authentication system."""
    if request.method == 'GET':
        if request.user.is_authenticated():
            return Response(
                {
                    'status': 'isLoggedIn'
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                'status': 'notLoggedIn'
            }, status=status.HTTP_401_UNAUTHORIZED
        )

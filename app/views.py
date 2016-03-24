from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.models import SocialAuthUsersocialauth


# Create your views here.
def index(request):
	"""Display the login template."""
	return render(request, 'views/angular_base.html', {'request': request})


@api_view(['GET'])
def is_logged_in(request):
	"""Method view to check if request is coming from a user who is logged in.

	This view checks whether the current user is logged in through a Django
	backends authentication system.	Return logged in status, user's first, last
	name and user's facebook id. The latter is used to retrieve the user's photo
	from Facebook's graph API.
	"""
	if request.method == 'GET':
		if request.user.is_authenticated():
			try:
				fbObject = SocialAuthUsersocialauth.objects.get(user=request.user)
				return Response(
					{
						'status': 'isLoggedIn',
						'username': request.user.first_name + ' ' + request.user.last_name,
						'uid': fbObject.uid
					}, status=status.HTTP_200_OK
				)
			except SocialAuthUsersocialauth.DoesNotExist:
				return Response(
					{
						'status': 'authenticated via Django default auth'
					}, status=status.HTTP_200_OK
				)
		return Response(
			{
				'status': 'notLoggedIn'
			}, status=status.HTTP_401_UNAUTHORIZED
		)

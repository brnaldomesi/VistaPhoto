from rest_framework import permissions


class IsOwner(permissions.BasePermission):
	"""Permissions restricting photo access to owners of the photos.
	"""

	def has_object_permission(self, request, view, obj):
		"""Method to check if incoming 'request' is from the owner of the obj.
		"""
		return obj.owner == request.user


class IsEditOwner(permissions.BasePermission):
    """Permissions restricting photo edit access to owners of the photos.
    """

    def has_object_permission(self, request, view, obj):
        """Method to check if incoming 'request' is from the owner of the obj.
        """
        return obj.photo.owner == request.user

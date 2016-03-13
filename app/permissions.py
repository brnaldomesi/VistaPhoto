from rest_framework import permissions


class IsOwner(permissions.BasePermission):
	"""Permissions restricting photo access to owners of the photos."""

	def has_object_permissions(self, request, view, obj):
		return obj.owner == request.user

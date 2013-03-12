from core.models import Repository
from core.serializers import RepositorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet
        return obj.owner == request.user
        
class RepositoryList(generics.ListCreateAPIView):
    model = Repository
    serializer = RepositorySerializer

    permission_classes = [
        IsOwnerOrReadOnly 
    ]
    
    def pre_save(self, obj):
        obj.owner = self.request.user

class RepositoryDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Repository
    serializer_class = RepositorySerializer

    permission_classes = [
        IsOwnerOrReadOnly
    ]
    
    def pre_save(self, obj):
        obj.owner = self.request.user

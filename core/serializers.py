from rest_framework import serializers

from core.models import Repository

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = [ 'id', 'name', 'owner' ]

    owner = serializers.Field(source='owner.username')

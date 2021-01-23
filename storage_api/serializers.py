from storage_api.models import FilesStatusModel
from rest_framework import serializers


class FilesStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilesStatusModel
        fields = [
            'hash_name',
            'url',
            'zip',
            'status'
        ]

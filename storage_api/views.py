import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from storage_api.tasks import save_files
from storage_api.serializers import FilesStatusSerializer
from storage_api.models import FilesStatusModel


class ArchiveViewSet(APIView):
    def get(self, request, hash_name):
        try:
            archive_object = FilesStatusModel.objects.get(pk=hash_name)
            return Response({
                'status': archive_object.status,
                'url': archive_object.url
            },
                status=status.HTTP_200_OK)
        except FilesStatusModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        urls = request.data
        file_name = str(uuid.uuid1())
        try:
            serializer = FilesStatusSerializer(data={
                'hash_name': file_name,
                'urls': '',
                'status': 'processing'
            })
            if serializer.is_valid():
                serializer.save()
            save_files.delay(urls, file_name, serializer)
            return Response({'archive_hash': f'{file_name}'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

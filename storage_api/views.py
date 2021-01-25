import os
import uuid

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from storage_api.tasks import save_files
from storage_api.serializers import FilesStatusSerializer
from storage_api.models import FilesStatusModel
from backup.settings import STORAGE_PATH


class ArchiveViewSet(APIView):
    def get(self, request, hash_name):
        print(hash_name)
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
        urls = request.data['urls']
        file_name = str(uuid.uuid1())
        try:
            serializer = FilesStatusSerializer(data={
                'hash_name': file_name,
                'status': 'in-progress'
            })
            if serializer.is_valid():
                serializer.save()
                save_files.delay(urls, file_name)
                return Response({'archive_hash': f'{file_name}'}, status=status.HTTP_201_CREATED)
            return Response({'error': f'{serializer.errors}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)


class GetArchiveViewSet(APIView):
    def get(self, request, zip_name):
        file_path = f'{STORAGE_PATH}{zip_name}'
        print(file_path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as zip_file:
                response = HttpResponse(zip_file, content_type="application/zip")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        return Response(status=status.HTTP_404_NOT_FOUND)

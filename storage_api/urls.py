from django.urls import path, include
from storage_api.views import ArchiveViewSet

urlpatterns = [
    path('archive/create/', ArchiveViewSet.as_view()),
    path('archive/status/<str:hash_name>', ArchiveViewSet.as_view())
]

from django.db import models


class FilesStatusModel(models.Model):
    hash_name = models.CharField(max_length=50, primary_key=True)
    url = models.URLField()
    zip = models.FileField(blank=True)
    status = models.CharField(max_length=50)

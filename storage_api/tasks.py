import uuid

from celery import shared_task
import requests
import hashlib
from zipfile import ZipFile
from storage_api.models import FilesStatusModel


@shared_task()
def save_files(urls, file_name, file_object):
    pass
    # with ZipFile(f'{file_name}.zip', 'w') as zip_file:
    #     errors = 0
    #     for url in urls:
    #         try:
    #             file = requests.get(url, allow_redirects=True)
    #             zip_file.write(file)
    #
    #         except Exception:
    #             errors += 1

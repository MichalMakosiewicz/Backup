import os

from celery import shared_task
import requests
from zipfile import ZipFile
from storage_api.models import FilesStatusModel


def get_status(urls_len, errors):
    if urls_len == errors:
        return 'filed'
    elif errors != 0:
        return 'success with errors'
    elif errors == 0:
        return 'success'


@shared_task()
def save_files(urls, file_name):
    errors = 0
    with ZipFile(f'storage/{file_name}.zip', 'w') as zip_file:
        for url in urls:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                temp_file_name = url.split('/')[-1]
                open(temp_file_name, 'wb').write(r.content)
                zip_file.write(temp_file_name)
                os.remove(temp_file_name)
            else:
                errors += 1
    try:
        object_instance = FilesStatusModel.objects.get(pk=file_name)
        object_instance.status = get_status(len(urls), errors)
        if len(urls) != errors:
            object_instance.zip = f'storage/{file_name}.zip'
            object_instance.url = f'http://127.0.0.1:8000/archive/get/{file_name}.zip'
        object_instance.save()
    except Exception as e:
        print(e)

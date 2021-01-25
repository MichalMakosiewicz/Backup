# Backup
App to backup your files.

## Requirements
 - Docker 20.10.2
 - Docker-compose 1.25.0
  
 ## Setup
 
 - pull repository
 - in root dir run `sudo docker-compose build` and after that `sudo docker-compose up`
 - There should be 4 containers. You can check that with command `sudo docker ps`:
 
 ```
 CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS          PORTS                    NAMES
c255dda3d1aa   backup_celery   "celery -A backup wo…"   8 minutes ago   Up 22 seconds                            backup_celery_1
3f89bb957f92   backup_web      "python manage.py ru…"   8 minutes ago   Up 22 seconds   0.0.0.0:8000->8000/tcp   backup_web_1
45bb7dca197e   postgres        "docker-entrypoint.s…"   24 hours ago    Up 22 seconds   5432/tcp                 backup_db_1
7717cb8df9c3   redis:latest    "docker-entrypoint.s…"   24 hours ago    Up 22 seconds   6379/tcp                 backup_redis_1
 ```
 
 - You need to make migrations on DB, run:
 
    `sudo docker exec -it <CONTAINER ID> python manage.py migrate` - use id of backup_web
 
    `sudo docker exec -it <CONTAINER ID> python manage.py makemigrations` - use id of backup_web

- Your enviroment sould be setup and app is running on `http://127.0.0.1:8000/`.

## Endpoints

`POST`  `/api/archive/create/`

Creates zip archive with files from urls.

Headers:

```
"Content-Type": "application/json"
```

Body:

```
{
    "urls": ["https://www.pandasecurity.com/en/mediacenter/src/uploads/2013/11/pandasecurity-facebook-photo-privacy.jpg", "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"]
}
```

Response:

```
{
    "archive_hash": "ae568438-5f3d-11eb-9911-0242ac130004"
}
```

---

`GET`  `/api/archive/status/<archive_hash>/`

Checks status and url of created archive

Response:

```
{
    "status": "success",
    "url": "http://127.0.0.1:8000/archive/get/ae568438-5f3d-11eb-9911-0242ac130004.zip"
}
```

---

`GET` `/archive/get/<archive_name>.zip`

Download archive. (Works in Brave browser)

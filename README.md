# f23_team_14
Repository for f23_team_14

+ Install the package:
```
pip install django-cors-headers
pip install Pillow
```

+ Set up the model:

```
python manage.py makemigrations
python manage.py migrate
```
+ Then run server:
```
python manage.py runserver
```
+ Change fields in models?
remove db.sqlite3, then makemigrations & migrate again
+ You can start from a clean state with the following steps:
1. Commit your work (just in case you accidentally delete something you wish you hadn’t)
2. Delete the database (rm db.sqlite3)
3. Delete the migrations (rm -fr <appname>/migrations)
4. Make migrations (python manage.py makemigrations <appname>)
5. Migrate (python manage.py migrate)
6. Run (python manage.py runserver)

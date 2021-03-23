# Fatty
## Backend part of the Fatty project.

### Uses:
* [Python 3.9](https://www.python.org/downloads/)
* [Redis](https://redis.io/download)
* [PostgreSQL 12](https://www.postgresql.org/download/)
* [Django 3.1.7](https://docs.djangoproject.com/en/3.1/releases/3.1.7/)
* [DRF 3.12.2](https://www.django-rest-framework.org/community/release-notes/#312x-series)
* [Huey 2.3.1](https://huey.readthedocs.io/en/latest/index.html)

### How to run
1. Install python dependencies
   ```shell
    $ pip install -r requirements.txt
    ```
2. Create file `backend/settings_local.py` and fill it with your DB info and your secret key (you can delete SECRET_FIELD key if you want)
3. Init DB
   ```shell
   $ python manage.py migrate
   $ python manage.py createsuperuser
    ```
4. Run by 
    ```shell
    $ python manage.py runserver
    ```
   
If you have `citext` errors, run in terminal under `psql`
```shell
    user# \c <table_name>
    user# CREATE EXTENSION citext;
```
Where `<table_name>` is your DB table name
   
### To run Huey
1. Run redis in separate term window
    ```shell
    $ redis-server
    ```
2. Run huey in separate term window
    ```shell
    $ python manage.py run_huey
    ```

### To run tests
1. Do steps 1-3 from "How to run" section
2. Run tests with
    ```shell
    $ python manage.py test -v 3
    ```
3. If you need coverage run
    ```shell
    $ coverage run --source='.' manage.py test -v 3
    $ coverage report --skip-covered
    ```

If you have `citext` errors, run in terminal under `psql`
```shell
    user# \c test_<table_name>
    user# CREATE EXTENSION citext;
```
Where `<table_name>` is your DB table name.
Also, you will need to run tests with `--keepdb` key.
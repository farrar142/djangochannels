find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python3 manage.py makemigrations
python3 manage.py migrate
#celery multi start tasks -A mysite -l log
#python3 manage.py runserver 0.0.0.0:8021
celery -A mysite worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A mysite  worker -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
#celery -A mysite worker -l info
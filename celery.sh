
celery -A mysite worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
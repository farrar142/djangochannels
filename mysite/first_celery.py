from celery import Celery
app = Celery('my_first_celery')
app.config_from_object('celeryconfig')

@app.task
def multiple(x,y):
    return x+y
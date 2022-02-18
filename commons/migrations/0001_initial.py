# Generated by Django 4.0.2 on 2022-02-17 18:22

from django.db import migrations, models
from commons.models import *

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]
    
    def gen_code(App,Scheme_editor):
        type = ["BUY","SELL"]
        code = ["NORMAL","COMPLETE","CANCELED","HOLD","MARKET"]
        event = ["SIGNUP","EVENT1"]
        for i in type:
            Type(type=i).save()
        for i in code:
            Code(code=i).save()
        for i in event:
            Event(event=i).save()

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('code_id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('event', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.RunPython(gen_code)
    ]

# Generated by Django 4.0.1 on 2022-02-01 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_name', models.CharField(max_length=20, verbose_name='유저이름')),
                ('p_name', models.CharField(max_length=20, verbose_name='상품이름')),
                ('price', models.IntegerField(verbose_name='거래가격')),
                ('status', models.CharField(max_length=20, verbose_name='거래유형')),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='게시날짜')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='거래가격')),
                ('status', models.CharField(choices=[('매도', 'Sell'), ('매입', 'Buy')], max_length=20, verbose_name='거래유형')),
                ('reg_date', models.DateTimeField(auto_now_add=True, verbose_name='게시날짜')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 3.0 on 2020-01-21 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pyuploadcare.dj.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mysalon', '0003_item_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salonposts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('pic', pyuploadcare.dj.models.ImageField(blank=True)),
                ('price', models.FloatField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1000)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysalon.Salonposts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 2.2.7 on 2019-11-21 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='expired_at',
            field=models.DateTimeField(default=''),
        ),
    ]
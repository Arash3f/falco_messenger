# Generated by Django 3.2.3 on 2021-06-26 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='members',
            name='date_join',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterUniqueTogether(
            name='groupchat',
            unique_together={('slug', 'name')},
        ),
    ]
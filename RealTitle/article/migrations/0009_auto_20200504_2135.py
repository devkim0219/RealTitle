# Generated by Django 2.2.5 on 2020-05-04 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='media_acc',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='result_acc',
            field=models.FloatField(null=True),
        ),
    ]
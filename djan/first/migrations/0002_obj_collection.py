# Generated by Django 4.1.2 on 2022-10-12 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='obj',
            name='collection',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
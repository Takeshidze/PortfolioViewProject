# Generated by Django 4.1.2 on 2022-10-20 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0006_alter_galery_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galery',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='first/static/image/'),
        ),
    ]
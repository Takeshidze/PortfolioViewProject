# Generated by Django 4.1.2 on 2022-10-28 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0017_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
    ]
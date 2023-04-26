import os

from django.conf import settings
from django.db import models

from djan.settings import STATIC_IMAGES


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category


class Objects(models.Model):
    object = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.object


class Movement(models.Model):
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField(null=True)
    first_location = models.ForeignKey(Objects, on_delete=models.CASCADE, related_name="first")
    second_location = models.ForeignKey(Objects, on_delete=models.CASCADE, related_name="second")


class Galery(models.Model):
    author = models.CharField(max_length=255, null=True)
    sizeX = models.IntegerField(null=True)
    sizeY = models.IntegerField(null=True)
    obj = models.ForeignKey('Objects', on_delete=models.SET_NULL, null=True)
    img = models.ImageField(upload_to='images/', default='static_images/default.jpg', null=True)
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=1023, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(null=True)
    dir = models.CharField(max_length=255, null=True)
    material = models.CharField(max_length=255, null=True)
    movements = models.ManyToManyField(Movement)

    def delete(self):
        obj = Galery.objects.get(id=self.id)
        if obj.img.path != STATIC_IMAGES + '\default.jpg':
            os.remove(self.img.path)
        return super(Galery, self).delete()

    def save(self, **kwargs):
        try:
            obj = Galery.objects.get(id=self.id)
            if obj.img.path != self.img.path and obj.img.path != STATIC_IMAGES + '\default.jpg':
                os.remove(obj.img.path)
        except:
            pass
        return super(Galery, self).save(**kwargs)

    def get_absolute_url(self):
        return f'/pictures/{self.id}'

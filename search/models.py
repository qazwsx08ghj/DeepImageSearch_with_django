from django.db import models

# Create your models here.


def nameFile(instance, filename):
    return '/'.join(['images', str(instance.image_name), filename])


class Image(models.Model):
    image_name = models.CharField(max_length=256)
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)

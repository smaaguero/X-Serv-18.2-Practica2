from django.db import models


# Create your models here.
class Url(models.Model):
    adress = models.TextField()

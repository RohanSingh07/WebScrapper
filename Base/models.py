from django.db import models

# Create your models here.
class Urlword(models.Model):
    url = models.TextField()
    words = models.ManyToManyField('Word')


class Word(models.Model):
    word = models.CharField(max_length=60)
    frequency = models.IntegerField()
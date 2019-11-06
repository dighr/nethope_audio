from django.db import models


# Create your models here.
class AudioFiles(models.Model):
    filename = models.CharField(max_length=1000)
    timestamp = models.CharField(max_length=1000)
    phonenumber = models.CharField(max_length=1000)
    transcription = models.CharField(max_length=1000)
    translation = models.CharField(max_length=1000)
    processed = models.IntegerField()


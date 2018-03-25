from __future__ import unicode_literals

from django.db import models

# Create your models here.
class genre(models.Model):
    user = models.CharField(max_length=200)
    genreS = models.CharField(max_length=200)
    def __str__(self):
        return self.user

# from mongoengine import Document, StringField, IntField
from django.db import models

class Evento(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    organizer = models.CharField(max_length=255)
    time = models.TimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.TextField(blank=True)

    def __str__(self):
        return self.title

from django.db import models

# Create your models here.
class Entry(models.Model):
	timestamp = models.DateTimeField()
	personnel = models.CharField(max_length=80)
	item = models.CharField(max_length=80)
	qty = models.IntegerField()

class Item(models.Model):
	name = models.CharField(max_length=80)
	qty = models.IntegerField()
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
	title = models.CharField(max_length = 100)
	author = models.ForeignKey( User, on_delete = models.CASCADE) 
	pages = models.IntegerField()
	publication = models.CharField(max_length = 100)

	def __str__(self):
		return self.title


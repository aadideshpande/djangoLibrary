from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Book(models.Model):
    title           = models.CharField(max_length=100)
    author          = models.CharField(max_length=100)
    publication		= models.CharField(max_length=100)	
    myuser          = models.ForeignKey( User,
                                            on_delete = models.CASCADE
                                        )   
    def __str__(self):
        return self.title

    # after a new book is created, user is sent to
    # the detail view of the new book
    def get_absolute_url(self):
    	return reverse('book-detail', kwargs={'pk' : self.pk})
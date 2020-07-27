from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# we are using this to keep constraints for the user age
from django.core.validators import MaxValueValidator, MinValueValidator

# for the phone number field
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.




class Profile(models.Model):
	GENDER = (
		('M', 'male'),
		('F', 'female'),
	)
	# one to one relationship with the existing
	# user model

	# CASCADE: if user is deleted, delete the profile but not
	# vice versa
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	age = models.IntegerField(
			default = 1, 
			validators=[MaxValueValidator(120), MinValueValidator(1)]
		)
	phone = PhoneNumberField()
	gender = models.CharField(max_length = 1, choices=GENDER)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')


	def __str__(self):
		return f'{self.user.username} Profile'


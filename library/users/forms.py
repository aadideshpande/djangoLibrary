from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# we inherit the UserCreationForm
class UserRegisterForm(UserCreationForm):
	
	# we add a new field to add email
	email = forms.EmailField()

	# this form interacts with the user mode
	# when form validates, it will create a new user
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
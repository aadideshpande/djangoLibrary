from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# function for new user registeration
def register(request):

	# if the user is going to add data in the database i.e POST  
    if request.method == 'POST':

    	# the new form has the data from request.POST
        form = UserRegisterForm(request.POST)
        print(form)

        # check the validity of the form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in')

            # if data is valid, we redirect the user to the home page
            # and success message is displayed
            return redirect('login')
        #else:
            #messages.info(request, f'Enter the information according to the instructions')
            #return redirect('register')   
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form' : form})


# we add a decorator to the view, 
# to prevent any user from manually going to the
# profile page.
@login_required
# function for user's profile
def profile(request):
    return render(request, 'profile.html')



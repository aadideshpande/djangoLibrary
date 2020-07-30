from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from books.models import Book
from django.contrib.auth.models import User
from fav.models import Favorite
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
    curr_user = request.user
    curr_books = curr_user.book_set.all()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated !')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    book_id_list = []
    favs = Favorite.objects.all()

    # to print the favorite books of the user
    for i in favs:
        if i.user == request.user:
            k = i.target_object_id

            if Book.objects.filter(id=k).exists():
                myobj = Book.objects.get(id=k)
                #print(type(myobj))
                book_id_list.append(myobj)
                #print(type(book_id_list))


    if len(book_id_list) == 0:
        empty = True
    else:
        empty = False

    context = {
    'u_form':u_form,
    'p_form':p_form,
    'curr_books': curr_books,
    'fav_books' : book_id_list,
    'empty' : empty
    }
    return render(request, 'profile.html', context)


def home(request):
    all_books = Book.objects.all()
    context = {
        'books' : all_books
    }
    return render(request, 'base.html', context)
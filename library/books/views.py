from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from fav.models import Favorite
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
class BookListView(ListView):
	model = Book

	# name of the html file in which the view is
	# to be displayed
	template_name = 'base.html'
	
	# default name is 'objects', but 
	# {% for book in books %} in base.html
	# we want to use 'books'
	context_object_name = 'books'
	paginate_by = 5



class BookDetailView(LoginRequiredMixin,DetailView):
	model = Book
	def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            fav_list1 = []
            #fav_list2 = []

            fav_list1 = Favorite.objects.filter(user = self.request.user, target_object_id = context['object'].id)

            # user should be able to add the book to his favorites
            # only if he is not the owner of the book
            if self.request.user == context['object'].myuser:
                context['not_same_user'] = False
                return context
            else:
                context['not_same_user'] = True
            
            '''
            for i in fav_list1:
                if i.target_object_id == context['object'].id:
                    fav_list2.append(i)
            '''

            if len(fav_list1) == 0:
                context['notpresent'] = True
            else:
                context['notpresent'] = False
            return context

"""
def book_detail(request, id):
	book = get_object_or_404(Book, id=id, slug=slug)
	context = {
		'object' : book,
	}
	return render(request, 'books/book_detail.html', context_object_name)



"""


# LoginRequiredMixin is used in case the user tries to
# go to book/new/ to create a new book without logging in
# he/she is redirected to the login page
class BookCreateView(LoginRequiredMixin,CreateView):
	model = Book
	fields = ['title', 'author', 'publication']

	# the creator of the new book should be
	# the current logged in user
	def form_valid(self, form):
		form.instance.myuser = self.request.user
		return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
	model = Book
	fields = ['title', 'author', 'publication']

	def form_valid(self, form):
		form.instance.myuser = self.request.user
		return super().form_valid(form)

	# is the user who is updating the book , the 
	# same user who created the post?
	def test_func(self):
		book = self.get_object()
		if self.request.user == book.myuser:
			return True
		else:
			return False

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
	model = Book
	success_url = '/'

	def test_func(self):
		book = self.get_object()
		if self.request.user == book.myuser:
			return True
		else:
			return False

# function for our search bar
def search(request):

	# we get the query from the search bar
	query = request.GET['query']

	# To prevent large queries to be searched on our page,
	# we put a condition
	if len(query) > 100:
		obj = Book.objects.none()
	else:
		# if title of the object contains the query, 
		# we filter it
		objTitle = Book.objects.filter(title__icontains=query)
		objAuthor = Book.objects.filter(author__icontains=query)

		# we perform a union of both the searches to prevent duplicates
		obj = objTitle.union(objAuthor)

	if obj.count() == 0:
		messages.warning(request, f'No results found')
	context = {
		'searchbooks' : obj,
		'query' : query,
	}
	return render(request, "search.html", context)



@login_required
def favorite_book(request, pk):
       book1 = get_object_or_404(Book, id=pk)
       print(book1)
       user1 = request.user
       print(user1)
       fav = Favorite.objects.create(user1, book1)
       print(fav)
       messages.success(request, f'This post has been added to your favorites')

       return  HttpResponseRedirect(book1.get_absolute_url())


@login_required
def remove_favorite_book(request, pk):
       book1 = get_object_or_404(Book, id=pk)
       print(book1)
       user1 = request.user
       print(user1)
       fav = Favorite.objects.filter(user = user1, target_object_id = pk)
       print(fav)
       fav.delete()
       messages.success(request, f'This post has been removed from your favorites')

       return  HttpResponseRedirect(book1.get_absolute_url())


@login_required
def remove_favorite_book2(request, pk):
       book1 = get_object_or_404(Book, id=pk)
       print(book1)
       user1 = request.user
       print(user1)
       fav = Favorite.objects.filter(user = user1, target_object_id = pk)
       print(fav)
       fav.delete()
       #messages.success(request, f'This post has been removed from your favorites')

       return redirect('profile')
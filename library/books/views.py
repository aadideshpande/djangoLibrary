from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
class BookListView(ListView):
	model = Book

	# name of the html file in which the view is
	# to be displayed
	template_name = 'base.html'
	
	# default name is 'objects', but 
	# {% for book in books %} in base.html
	# we want to use 'books'
	context_object_name = 'books'

class BookDetailView(DetailView):
	model = Book


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

	# if title of the object contains the query, 
	# we filter it
	obj = Book.objects.filter(title__contains=query)
	context = {
		'searchbooks' : obj,
	}
	return render(request, "search.html", context)
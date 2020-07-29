from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
class BookListView(ListView):
	model = Book

	# name of the html file in which the view is
	# to be displayed
	template_name = 'base.html'
	
	# default name is 'objects', but 
	# {% for book in books %} in base.html
	# we want to use 'books'
	context_object_name = 'books'
	paginate_by = 4



class BookDetailView(DetailView):
	model = Book

"""
def book_detail(request, id):
	book = get_object_or_404(Book, id=id, slug=slug)
	context = {
		'object' : book,
	}
	return render(request, 'books/book_detail.html', context_object_name)




def favourite_book(request):
	book = get_object_or_404(Book, id = request.POST.get('book_id'))
	is_favourite = False
	if book.favourite.filter(id=request.user.id).exists():
		book.favourite.remove(request.user)
		is_favourite = False
	else:
		is_favourite = True
		book.favourite.add(request.user)
	return  HttpResponseRedirect(book.get_absolute_url())
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
		objTitle = Book.objects.filter(title__contains=query)
		objAuthor = Book.objects.filter(author__contains=query)

		# we perform a union of both the searches to prevent duplicates
		obj = objTitle.union(objAuthor)

	if obj.count() == 0:
		messages.warning(request, f'No results found')
	context = {
		'searchbooks' : obj,
		'query' : query,
	}
	return render(request, "search.html", context)


"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from books import views as books_views
# this is provided by django for login and logout
from django.contrib.auth import views as auth_views

# for adding the roots for media url
from django.conf import settings
from django.conf.urls.static import static

from books.views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BookListView.as_view(), name='home'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    #path('book/<int:pk>', book_detail, name='book-detail'),
    path('book/<int:pk>/update', BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete', BookDeleteView.as_view(), name='book-delete'),
    path('book/new/', BookCreateView.as_view(), name='book-create'),
    #path('', user_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('search/',books_views.search, name='search'),
    path('favorite/<int:pk>', books_views.favorite_book, name='favorite_book'),
    path('removefavorite/<int:pk>', books_views.remove_favorite_book, name='remove_favorite_book'),
    path('removefavorite2/<int:pk>', books_views.remove_favorite_book2, name='remove_favorite_book2'),

    path('profile/<int:pk>', user_views.view_profile, name='view_profile'),
    path('adminstats/', user_views.adminstats, name='adminstats'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


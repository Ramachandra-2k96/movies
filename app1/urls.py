# urls.py
from django.urls import path
from .views import upload_file,search_movies,land,login_view,logout_view,home,movie_detail,profile,add,search

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('', land, name='land'),
    path('home', home, name='home'),
    path('out', logout_view, name='logout'),
    path('add/<int:movie_id>/', add, name='add'),
    path('login', login_view, name='login'),
    path('search', search, name='search'),
    path('profile', profile, name='profile'),
    path('ajax/search/', search_movies, name='search_items'),
    path("movie_detail/<int:movie_id>/", movie_detail, name="movie_detail")
]

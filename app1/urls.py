# urls.py
from django.urls import path
from .views import upload_file,search_items,land,login_view,logout_view,home,movie_detail

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('', land, name='land'),
    path('home', home, name='home'),
    path('out', logout_view, name='logout'),
    path('login', login_view, name='login'),
    path('ajax/search/', search_items, name='search_items'),
    path("movie_detail/<int:movie_id>/", movie_detail, name="movie_detail")
]

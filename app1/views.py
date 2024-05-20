from random import Random
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import UploadFileForm,CustomAuthenticationForm,CustomUserCreationForm
import pandas as pd
from .models import Movies
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.models import AnonymousUser

def land(request):
    random_movies=Movies.objects.filter(gener__icontains="Action").order_by('?')[:15]
    return render(request, 'app1/index.html',{'search_results': list(random_movies.values('id','title', 'image', 'date', 'gener', 'rating', 'description'))})


def login_view(request):
	if request.method == 'POST':
		log = CustomAuthenticationForm(request, data=request.POST)
		sin = CustomUserCreationForm(request.POST)	
		if log.is_valid():
			username = log.cleaned_data.get('username')
			password = log.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				return render(request, 'app1/form.html', {'form1': log,"form2":sin})
		else:
			if sin.is_valid():
				sin.save()
				user = authenticate(username=sin.cleaned_data['username'], password=sin.cleaned_data['password1'])
				login(request, user)
				return redirect('home')
			else:
				return render(request, 'app1/form.html', {'form1': log,"form2":sin,'error_message': 'Invalid username or password'})
	else:
         if isinstance(request.user, AnonymousUser):
            log = CustomAuthenticationForm()
            sin = CustomUserCreationForm()
            return render(request, 'app1/form.html', {'form1': log,"form2":sin})
         else:
            return redirect('home')
        
def home(request):
    if isinstance(request.user, AnonymousUser):
        return redirect('login')
    else:
        random_movies=Movies.objects.filter(gener__icontains="Action").order_by('?')[:15]
        recomendation=list(random_movies.values('id','title', 'image', 'date', 'gener', 'rating', 'description'))
        
        random_movies=Movies.objects.filter(rating__gte=8.0).order_by('?').exclude(gener__icontains="Romance")[:20]
        popular=list(random_movies.values('id','title', 'image', 'date', 'gener', 'rating', 'description'))
        
        random_movies=Movies.objects.filter(gener__icontains="Action",rating__gte=7.0).order_by('?')[:20]
        action=list(random_movies.values('id','title', 'image', 'date', 'gener', 'rating', 'description'))
        
        random_movies=Movies.objects.filter(gener__icontains="Drama",rating__gte=7.0).order_by('?')[:20]
        drama=list(random_movies.values('id','title', 'image', 'date', 'gener', 'rating', 'description'))
        
        random_movies=Movies.objects.filter(gener__icontains="Science Fiction",rating__gte=7.0).order_by('?')[:20]
        Science_Fiction=list(random_movies.values('id','title', 'image', 'date', 'gener', 'rating', 'description'))
        
        random_movies=Movies.objects.filter(gener__icontains="Comedy",rating__gte=7.0).order_by('?')[:20]
        Comedy=list(random_movies.values('id','title', 'image', 'date', 'gener', 'rating', 'description'))
        
        return render(request, 'app1/home.html',{'recomendation':recomendation,"popular":popular,"action":action,"Comedy":Comedy,"Science_Fiction" :Science_Fiction,"drama":drama})


def profile(request):
    user=request.user
    return render(request,"app1/profile.html",{"user":user})

def logout_view(request):
	logout(request)
	return redirect('login')

def search_items(request):
    query = request.GET.get('query', '')
    items = Movies.objects.filter(title__istartswith=query)[:25]
    return JsonResponse(list(items.values('id','title', 'image', 'date', 'gener', 'rating', 'description')), safe=False)


def add(request,movie_id):
    return HttpResponse("<h1>Development in progress, please come again after some time</h1>")

def search(request):
    return HttpResponse("<h1>Development in progress, please come again after some time</h1>")

def movie_detail(request,movie_id):
    if isinstance(request.user, AnonymousUser):
        return redirect('login')
    else:
        from datetime import datetime
        movie=Movies.objects.get(id=movie_id)
        formatted_date = movie.date.strftime("%Y-%B-%d")
        mov={
            'title':movie.title,
            'image':movie.image,
            'date':formatted_date,
            'gener':movie.gener,
            'rating':movie.rating,
            'description':movie.description
        }
        print(formatted_date)
        return render(request,'app1/movie_detail.html',{'movie':mov})

def upload_file(request):
    if request.method == 'POST':
        chunk_size = 1000
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Save the uploaded file to a temporary location
            with open(file.name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.seek(0)  # Reset file pointer to start

            try:
                df = pd.DataFrame()
                with open(destination.name, 'r') as file:
                    for chunk in pd.read_csv(file, chunksize=chunk_size):
                        df = pd.concat([df, chunk], ignore_index=True)

                # Process dataframe and save to database
                for index, row in df.iterrows():
                    # Check for null or empty values and handle them accordingly
                    image = row[5] if row[5] and row[5] != 'nan' else "https://www.peacemakersnetwork.org/wp-content/uploads/2019/09/placeholder.jpg"
                    rating = float(row[3]) if row[3] and row[3] != 'nan' else 3.3

                    Movies.objects.get_or_create(
                        title=row[1],
                        defaults={
                            'image': image,
                            'date': row[0],
                            'gener': row[4],  # Assuming 'gener' is supposed to be 'genre'
                            'rating': rating,
                            'description': row[2],
                        }
                    )

                return JsonResponse({'success': 'File uploaded successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)})
            finally:
                os.remove(destination.name)
        else:
            print(form.errors)
            return JsonResponse({'error': 'Invalid form'})
    else:
        form = UploadFileForm()
    return render(request, 'app1/upload.html', {'form': form})


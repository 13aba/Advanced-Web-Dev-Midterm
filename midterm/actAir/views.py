from django.shortcuts import render

# Create your views here.
#Everything below here are written by me 


#index page for the api links
def index(request):
    return render(request, 'index.html')
from django.shortcuts import render

# Create your views here.
#Everything below here are written by me 


def index(request):
    return render(request, 'index.html')
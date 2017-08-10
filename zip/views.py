from django.shortcuts import render

# Create your views here.

def hello (request):
    return render(request, 'zip.html')

def cat (request):
    return render(request, 'cat.html')


def add (request):
    return render(request, 'add.html')

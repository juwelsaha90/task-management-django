from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('Welcome to Task Management system')

def contact(request):
    return HttpResponse('This is contact page')

def show_tasks(request):
    return HttpResponse('This is show tasks page')

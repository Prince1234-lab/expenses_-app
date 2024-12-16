from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def userperferences(request):
    return HttpResponse('User Preferences App is working!')
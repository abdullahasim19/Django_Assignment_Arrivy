from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def bank_index(request):
    return HttpResponse('Bank App')


def homepage(request):
    return HttpResponse('Welcome')
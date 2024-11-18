from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    return render(request,template_name= 'SecondSpin/home')

def about(request):
    return render(request,template_name= 'SecondSpin/about')

def product_category(request):
    return render(request,template_name= 'SecondSpin/product_category')
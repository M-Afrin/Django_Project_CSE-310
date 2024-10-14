from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,template_name= 'SecondSpin/home.html')

def about(request):
    return render(request,template_name= 'SecondSpin/about.html')

def product_category(request):
    return render(request,template_name= 'SecondSpin/product_category.html')
from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, 'singel_page/landing.html')
def about_me(request):
    return render(request, 'singel_page/about_me.html')
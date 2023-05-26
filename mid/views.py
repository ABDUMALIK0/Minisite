from django.shortcuts import render
from .models import Staff
# Create your views here.
def index(request):
    return render(request, 'blog/reference.html')

def name_card(request, pk):
    item = Staff.objects.get(pk=pk)
    context = {
        'item': item,
    }
    return render(request, 'blog/name_card.html', context)

def name_card2(request, pk):
    item = Staff.objects.get(pk=pk)
    context = {
        'item': item,
    }
    return render(request, 'blog/name_card2.html', context)

def list(request):
    items = Staff.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'blog/list.html', context)
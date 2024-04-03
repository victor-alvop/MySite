from django.shortcuts import render
from django.http import HttpResponse 
from .models import item 
from django.template import loader

# Create your views here.
def index(request):
    item_list = item.objects.all()
    context={
        'item_list': item_list,
    }
    return render(request, 'food/index.html', context)

def items(request):
    return HttpResponse('<h1>This is an item view<h1>')

def detail(request, item_id):
    item_selected = item.objects.get(pk=item_id)
    context = {
        'item_selected': item_selected,
    }
    return render(request, 'food/details.html', context)

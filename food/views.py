from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .models import item 
from django.template import loader
from .forms import ItemForm

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

def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('food:index')

    return render(request, 'food/item-form.html', {'form': form})

def update_item(request, item_id):
    item_selected = item.objects.get(id=item_id)
    form = ItemForm(request.POST or None, instance=item_selected)

    if form.is_valid():
        form.save()
        return redirect('food:index')
    
    return render(request,'food/item-form.html', {'form':form, 'item':item_selected})

def delete_item(request, item_id):
    item_selected = item.objects.get(id=item_id)

    if request.method == 'POST':
        item_selected.delete()
        return redirect('food:index')

    return render(request,'food/delete_item.html',{'item':item_selected} )


from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    title = 'Welcome: This is the Home Page'
    form = 'Welcome: This is the Home Page'
    context = {
        'title':title,
        'test': form,
    }

    return render(request, "home.html", context)


@login_required  
def list_items(request):
    title = 'LIST OF ITEMS'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        'title':title,
        'queryset' : queryset,
        'form' : form,
    }

    if request.method == 'POST':
        queryset = Stock.objects.filter(#category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value()
        
                                        )
        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')  
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quality])
            return response                              
        context = {
            "form":form,
            'title':title,
            "queryset":queryset,
        }
    return render(request, "list_items.html", context)
@login_required    
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully saved')
        return redirect('/list_items')
    context = {
        "form": form,
        "title": "Add Item",
    }

    return render(request, "add_items.html", context)    

    
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully saved')
            return redirect('/list_items')
    context = {
        'form':form
    }
    return render(request, 'add_items.html', context)

def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deleted Successfully ')
        return redirect('/list_items')


    return render(request, 'delete_items.html')

def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset
    }

    return render(request, "stock_detail.html", context)

def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit = False)

        instance.quality -= instance.issue_quantity 

        instance.issue_by = str(request.user)

        messages.success(request, "Issued SUCCESSFULLY." + str(instance.quality)+" "+ str(instance.item_name)+"s now left in Store")
        instance.save()

        return redirect('/stock_detail/' + str(instance.id))
        #return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Issue' + str(queryset.item_name),
        "form": form,
        "username": 'Issue By:' +str(request.user),
    }

    return render(request, "add_items.html", context)

def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.quality += instance.receive_quantity 

        instance.save()
        messages.success(request, "Received SUCCESSFULLY." + str(instance.quality) +" "+ str(instance.item_name)+"s now in Store")

        return redirect("/stock_detail/" + str(instance.id))

    context ={
        "title":'Receive'+str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": 'Receive By:' + str(request.user),
    }

    return render(request, "add_items.html", context)

def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)

    if form.is_valid():
        instance = form.save( commit = False)
        instance.save()
        messages.success(request, "Reorder Level for "+ str(instance.item_name) +"is updated to" + str(instance.reorder_level))

        return redirect("/list_items")
    context = {
        "instance": queryset,
        "form":form,
    }
    return render(request, "add_items.html", context)



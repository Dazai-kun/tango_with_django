from rango.models import Page
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context_dict)
def about(request):
    context_dict2 = {'my_name': 'Huy'}
    return render(request, 'rango/about.html', context=context_dict2)
def show_category(request, category_name_slug):
    #create a context dict which we can pass to the template rendering
    #engine
    context_dict = {}
    try:
        #if we can't find a categoryn name slug with the given name
        #the .get() method raises a DoesNotExist exceptionself.
        #so the .get() method returns 1 model instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)
        #Retrieve all of the associated pagesself.
        #Note that filter() will return a list of page objects or an empty one
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, rango/category.html, context_dict)

from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'category': category_list}

    return render(request, 'rango/index.html', context=context_dict)
def about(request):
    context_dict2 = {'my_name': 'Huy'}
    return render(request, 'rango/about.html', context=context_dict2)

from datetime import datetime
from rango.forms import UserForm, UserProfileForm
from rango.forms import PageForm
from rango.forms import CategoryForm
from rango.models import Page
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
def register(request):
    registered = False
# If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form = UserForm(data=request.POST)
            profile_form = UserProfileForm(data=request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
# Now we hash the password with the set_password method.
# Once hashed, we can update the user object.
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']
                profile.save()
                registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
            user_form = UserForm()
            profile_form = UserProfileForm
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'register': registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

#We use request.POST.get('<variable>') as opposed
# to request.POST['<variable>'], because the
# request.POST.get('<variable>') returns None if the
# value does not exist, while request.POST['<variable>']# will raise a KeyError exception.
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
         return render(request, 'rango/login.html', {})
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val




def index(request):
    request.session.set_test_cookie()
    page_list = Page.objects.order_by('views')[:5]
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'rango/index.html', context_dict)

    return response
def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE worked")
        request.session.delete_test_cookie()
    visitor_cookie_handler(request)
    context_dict2 = {'my_name ': 'Huy'}
    context_dict2['visits'] = request.session['visits']
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

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid:
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, "category":category}
    return render(request, 'rango/add_page.html', context_dict)

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

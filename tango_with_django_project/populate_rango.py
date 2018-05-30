import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page
def populate():
    #python_cat = add_cat('Python', views=128, likes=64)
    python_pages = [
        {'title': 'Official Python Tutorial',
          'url': 'http://docs.python.org/2/tutorial/' },
        {'title': 'How to think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/'},
        {'title': 'Learn python in 10mins',
         'url': 'http://www.korokithakis.net/tutorials/python/'}
]
    #django_cat = add_cat('Django', views=64, likes=32)
    django_pages = [
    {'title': 'Official Django Tutorial', 'url': 'https://docs.djangoproject.com/en/1.9/intro/tutorial01/' },
    {'title': 'Django Rocks', 'url': 'http://www.djangorocks.com/'},
    {'title': 'How to Tango with Djano', 'url': 'http://www.tangowithdjango.com/'}
    ]
    #other_cat = add_cat('Other Frameworks', views=32, likes=16)
    other_pages = [
    {'title': 'Bottle', 'url':'http://bottlepy.org/docs/dev/'},
    {'title': 'Flask', 'url':'http://flask.pocoo.org'}
    ]
    cats = {'Python': {'pages': python_pages, 'likes': 64, 'views': 128},
            'Django': {'pages': django_pages, 'likes': 32, 'views': 64},
            'Other Frameworks': {'pages': other_pages, 'likes': 16, 'views': 32} }
#there r now 3 Categories, each category has the pages as above.
    for cat, cat_data in cats.items(): #cats.items = [('Python', ('pages', 'python_pages')]
        c = add_cat(cat, cat_data['likes'], cat_data['views']) # this will basically add the categories Python, Djano and Other Frameworks
        for p in cat_data['pages']: # cat_data[pages] = python_pages
            add_page(c, p['title'], p['url']) # it will add the pages into the category

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print('- {0} - {1}'.format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title) [0] #create page according to the 3 categories by title
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, likes, views):
    c = Category.objects.get_or_create(name=name) [0] # create the categories by name
    c.views = views
    c.likes = likes
    c.save() # then save it
    return c

if __name__ == '__main__':
    print('Starting Rango population script.....')
    populate()

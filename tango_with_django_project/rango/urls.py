from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$' ,
        views.show_category, name='show_category'),
# the regular expression [\w\-]+) will look for
#any sequence of alphanumeric characters e.g. a-z, A-Z,
#or 0-9 denoted by \w and any hyphens (-)
#denoted by \-, and we can match as many of
#these as we like denoted by the [ ]+ expression
   #url(r'^page/(?P<page_name_slug>[\w\-]+)/$' ,views.show_page, name='show_page'),
    url(r'^add_category/$', views.add_category, name='add_category'), 
]

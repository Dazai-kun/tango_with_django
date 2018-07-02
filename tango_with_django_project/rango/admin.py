from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
#The attribute prepopulated_fields tells the admin
#application to automatically fill
#the field slug - in this case with the text
#entered into the name field.


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

admin.site.register(UserProfile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)

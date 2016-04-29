from django.contrib import admin

# Register your models here.
from userdir.models import Person, City, Div

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mtel')

admin.site.register(Person, PersonAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'ccode')

admin.site.register(City, CityAdmin)

class DivAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'pri')

admin.site.register(Div, DivAdmin)


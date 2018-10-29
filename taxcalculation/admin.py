from django.contrib import admin

# Register your models here.
from taxcalculation.models import File, Person

admin.site.register(File)
admin.site.register(Person)

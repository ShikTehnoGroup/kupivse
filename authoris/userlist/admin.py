from django.contrib import admin

# Register your models here.
from .models import Person, User_employe

admin.site.register(Person)
admin.site.register(User_employe)
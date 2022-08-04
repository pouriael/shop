from django.contrib import admin
from .models import formprofile


class profile_admin(admin.ModelAdmin):
    list_display = ['user','phone','address']

admin.site.register(formprofile,profile_admin)


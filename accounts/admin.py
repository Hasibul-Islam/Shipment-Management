from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import CustomUser

admin.site.register(CustomUser)


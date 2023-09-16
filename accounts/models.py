from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    def __str__(self):
        return self.name


try: 
    admin_group = Group.objects.create(name='Admin')
    manager_group = Group.objects.create(name='Manager')
    
except:
    None
try:
    cnf_group = Group.objects.create(name='CNF')
except:
    None
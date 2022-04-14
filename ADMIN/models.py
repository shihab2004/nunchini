from customer.models import Profile
from re import T
from django.db import models

# Create your models here.
class chat_list(models.Model):
    admin_profile = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True,blank=True)
    lists = models.JSONField(max_length=5000,null=True,blank=True)
    
    def __str__(self):
        return str(self.admin_profile)
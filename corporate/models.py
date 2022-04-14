from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe
from django.core.validators import FileExtensionValidator
from root.models import Mobile ,Email
from customer.models import Profile
# Create your models here.
class root(models.Model):
    title = models.CharField(max_length=20)
    description = RichTextField(null=True,blank=True)
    image = models.ImageField(upload_to='corporate/root',null=True,blank=True)
    mobile = models.OneToOneField(Mobile,on_delete=models.SET_NULL,null=True,blank=True)
    email = models.OneToOneField(Email,on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return self.title

class Corporate(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(null=True,blank=True)
    is_show_in_index_page = models.BooleanField(default=False,null=True,blank=True)
    svg_file = models.FileField(upload_to="corporate/svg",validators=[FileExtensionValidator(["svg"])],default=None,null=True,blank=True)

    def __str__(self):
        return self.title

class Client(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    image = models.ImageField(upload_to='corporate/Client',null=True,blank=True)

    def image_tag(self):
        url = self.image.url
        return mark_safe('<img src="%s" width="90px" height="40px" />' % (url))


class Corporate_Customer(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.SET_NULL,null=True,default=None,related_name="get_corporate_customer")
    Business_Name = models.CharField(max_length=100)
    Phone_Number = models.PositiveIntegerField()
    Representative_Name = models.CharField(max_length=100,null=True,blank=True)
    Email_Address = models.EmailField()
    is_view = models.BooleanField(default=False,null=True,blank=True)


    def __str__(self):
        return self.Business_Name

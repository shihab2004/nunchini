from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse
from customer.models import Profile

# Create your models here.
class support_menu(models.Model):
    name = models.CharField(max_length=30)
    img = models.ImageField(upload_to='support/menu',null=True,blank=True)
    slug = models.SlugField(editable=False)
    body = RichTextField(null=True,blank=True)

    def __str__(self):
        return self.name
    
    def url(self):
        menu_slug = slugify(self.name)
        s_url = reverse('support:api')
        return f'{s_url}?menu={menu_slug}'

    def save(self,*args, **kwargs):
        self.slug = slugify(self.name)
        super(support_menu,self).save(*args, **kwargs)



class Team(models.Model):
    name = models.CharField(max_length=60)
    occupation = models.CharField(max_length=120,null=True,blank=True)
    photo = models.ImageField(upload_to='support/Team',null=True,blank=True)
    discription = RichTextField()

    def __str__(self):
         return self.name
ContactUs_choice =  (
        ("Y","Read"),
        ("N","New Mail"),
)

class ContactUs(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField()
    number = models.PositiveIntegerField(null=True,blank=True)
    message = models.TextField()
    status = models.CharField(max_length=2,choices=ContactUs_choice,default="N")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.profile:
            return self.profile.user.username
        return "Anonymous User"


from re import T
from django.db import models
from django.contrib.auth.models import User
from root.models import City,Area
from Product.models import Product



from django.core.validators import MaxValueValidator,MinValueValidator,RegexValidator        # Validator
# Create your models here.
gender_choises = (
    ("N","None"),
    ("M","Male"),
    ("F","Female"),
    ("O","Other")
)

class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="get_profile")
    profile_photo = models.ImageField(upload_to="customer/profile",null=True,blank=True)
        #validate number in next version
    Phone = models.PositiveIntegerField(verbose_name="Phone Number",null=True,blank=True)
    ip_addr = models.GenericIPAddressField()
    gender = models.CharField(max_length=1,choices=gender_choises)
    current_city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True,blank=True,related_name="get_current_profile",default=City.objects.first().pk)


    def __str__(self):
        return self.user.username if self.user else "None"
    
    def is_geoLocation(self):
            return True if self.location.get_queryset() else False

    def get_lat_long(self):
        location = self.location.get_queryset()[0]
        return {"lat":location.latitude,"lng":location.longitude}
    
    def get_all_adress(self):
        adress = self.adress.all().order_by("-pk")
        return adress

from uuid import uuid4
class Email_Verify(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.SET_NULL,null=True,blank=True)
    key = models.UUIDField(default=uuid4,primary_key=True)
    email = models.EmailField()

    def __str__(self):
        return self.profile.user.username





class ActiveUser(models.Model):
    profile = models.OneToOneField(Profile,related_name='get_active_status',on_delete=models.CASCADE)
    is_active =  models.BooleanField(default=False)

    def __str__(self):
        return self.profile.user.username


class user_adress(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="adress")
    adress = models.CharField(max_length=600)
    delivery_adress = models.BooleanField(blank=True,default=False)
    city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True)
    area = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True)
    delivery_parson_name = models.CharField(max_length=100,null=True,blank=True)
    Phone = models.PositiveIntegerField(verbose_name="Phone Number",null=True,blank=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user.username+ " - " + self.delivery_parson_name

    def get_latest_adress(self):
        return self.__class__.objects.order_by("updated_time").first()



class user_location(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="location")
    latitude = models.FloatField(validators=[MaxValueValidator(90),MinValueValidator(-90)])
    longitude = models.FloatField(validators=[MaxValueValidator(180),MinValueValidator(-180)])

    def __str__(self):
        return self.user.user.username
        
    def get_lat_long(self):
        return {"lat":self.latitude,"lng":self.longitude}

class Customer_bags(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    profile = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="get_customerBag_item")
    quantity = models.PositiveIntegerField(default=0)
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile.user.username + " :) " + self.product.Name
    
    
class C8Message(models.Model):
    roomId = models.IntegerField()
    profile = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name='get_profile_c8messages')
    message = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    is_rated  = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.profile.user.username + " - " + self.message[:20] + ("..." if len(self.message) >= 20 else "")
    

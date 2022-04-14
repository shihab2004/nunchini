
from tkinter.tix import Tree
from django.db import models
from django.db.models.expressions import F
from root.utils import image_or_link 
from django.utils.text import slugify
from root.models import Menu
from math import floor
from root.models import City,Payment_options_allow
from ckeditor.fields import RichTextField

# Create your models here.
class Delivery_man(models.Model):
    name = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="Product/Delivery_man",null=True,blank=True)
    
    def __str__(self):
        return self.name  
    
class Product(models.Model):
    
    Name = models.CharField(max_length=100)
    Price = models.FloatField(default=0)
    discord_price = models.PositiveIntegerField(default=0,null=True,blank=True)
    Amount = models.CharField(max_length=50, default=0,null=True,blank=True)
    Description = RichTextField(null=True,blank=True)
    Stoke_quantity = models.PositiveIntegerField(null=True,blank=True)
    menu = models.ManyToManyField(Menu,blank=True,related_name="product")
    slug = models.SlugField(verbose_name="Product slug",help_text="It use to facting product form url",null=True,blank=True)
    city = models.ManyToManyField(City,blank=True,related_name="city_related_product")
    offer_image = models.ImageField(upload_to="Product/Offer",null=True,blank=True)

    def __str__(self):
        return self.Name
    
    def get_discord_price(self):
        return int(self.Price) - int(self.discord_price)

    def save(self, *args, **kwargs):
        if not self.slug:
            full_slug = self.Name+" "+ self.Amount
            self.slug = slugify(full_slug)

        super(Product, self).save(*args, **kwargs)

    def percentage_off(self):
        if self.discord_price:
            divided_value = self.discord_price / self.Price
            off_percentage = floor(divided_value * 100)
            print("*********************************************")
            print(off_percentage)
            return off_percentage
        return None

    def is_discord_price(self):
        return True if self.discord_price else False
    
    def get_display_image(self):
        return self.product_image.get(is_main=True).get_image()





class Product_image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True,related_name="product_image")
    image = models.ImageField(upload_to="Product/",null=True,blank=True)
    image_link = models.URLField(null=True,blank=True)
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product.Name if self.product else "NONE"

    def get_image(self):
        return image_or_link(self.image,self.image_link)
        

order_status_choise = (
        ("PN","Pending"),
        ("PS","Processing"),
        ("SF","Successful"),
        ("CN","Cancelled"),
)
report_choise = (
    ("Product quality was bad","Product quality was bad"),
    ("Wrong product","Wrong product"),
    ("Missing product","Missing product"),
    ("Expired product","Expired product"),
    ("Missing Matol's","Missing Matol's"),
    ("I didn't like the packaging","I didn't like the packaging"),
    ("My order arrived late","My order arrived late"),
    ("Delivery man was unprofessional","Delivery man was unprofessional"),
    ("Other","Other"),
)
from customer.models import Profile ,user_adress,user_location
from json import loads
from django.http import HttpResponseBadRequest
from root.models import Delivery_Charge_record
from django.db.models import Max
from django.core.validators import RegexValidator

class Order(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,related_name="get_user_order")
    product = models.ManyToManyField(Product,blank=True)
    payment_method = models.ForeignKey(Payment_options_allow,on_delete=models.SET_NULL,null=True)
    order_status = models.CharField(max_length=2,choices=order_status_choise,default="PN")
    track_ip = models.GenericIPAddressField()
    home_adress = models.ForeignKey(user_adress,on_delete=models.SET_NULL,null=True,blank=True)
    delivery_time = models.DateTimeField()
    ordered_time = models.DateTimeField(auto_now_add=True)
    bag_json = models.TextField()
    reusableBag_price = models.PositiveIntegerField(blank=True)
    discount_offer = models.FloatField(blank=True,default=0,null=True)
    order_report = models.CharField(max_length=40,null=True,blank=True,choices=report_choise)
    stars = models.IntegerField(validators=[RegexValidator(regex=r'^[0-5]$')],null=True,blank=True)
    Instructions = models.TextField(null=True,blank=True)
    geo_location = models.ForeignKey(user_location,on_delete=models.SET_NULL,null=True,blank=True)
    delivery_man = models.ForeignKey(Delivery_man,on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return self.profile.user.username + " - " + self.get_order_number + " - " + self.get_order_status_display()
    
    def star_range(self):
        a =  self.stars if self.stars else 0
        return range(0,a)
    
    
    def nun_star_range(self):
        a =  self.stars if self.stars else 0
        return range(0,5 - a)
    
    def product_info(self):
        return loads(self.bag_json).get('data')
    
    @property
    def get_order_number(self):
        return f"#{self.pk}"
    
    def is_use_geo_location(self):
        return True if self.geo_location else False
    
    def get_lat_lng(self):
        return self.geo_location.get_lat_long()
        

    def product_total(self):
        order_bag_json = loads(self.bag_json)
        total_price = 0

        try:
            if order_bag_json['status'] == "successful" and order_bag_json["data"]:
                for bag in order_bag_json['data']:
                    total_price += bag['price'] * bag['quantity']

                return total_price
            elif order_bag_json['status'] == "successful" and not order_bag_json["data"]:
                return None
        except KeyError:
                return None

    def dp(self):
        a= 0
        if self.total_price(True):
            a = self.total_price(True)
        return a
    
    def total_price(self,discont_price=False):
        order_bag_json = self.bag_json
        if not self.product_total():
            return None

        total_price  = self.product_total()
            


        delivery_charge = self.order_delivery_charge()
        
        all_total_price = total_price + delivery_charge + self.reusableBag_price
        if self.discount_offer:
    
            then_Dis_order_Tprice = (all_total_price/100) * self.discount_offer

   
            return  "%.2f" % then_Dis_order_Tprice if discont_price else "%.2f" % (all_total_price -  then_Dis_order_Tprice)

        if discont_price:
            return 0

        return "%.2f" % all_total_price

    def order_delivery_charge(self):
        total_price  = self.product_total()
        delivery_charge = 29
   
        try:
            dpobj = Delivery_Charge_record.objects.filter(if_price__lte=total_price).aggregate(Max("if_price"))["if_price__max"]
            
            delivery_charge = Delivery_Charge_record.objects.get(if_price=dpobj).delivery_Charge
        except Delivery_Charge_record.DoesNotExist:
            pass
        return delivery_charge
        
    def get_description(self):
        return f"{self.payment_method.Name} [Chaldal Grocery #{self.pk}]"



class Product_Request(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,related_name='get_user_product_request')
    product = models.ForeignKey(Product,blank=True,related_name='get_all_user_request',on_delete=models.SET_NULL,null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile.user.username

from uuid import uuid4
class Special_Code(models.Model):
    discount_parsent = models.PositiveIntegerField(null=True,blank=True)
    code = models.CharField(default=uuid4,max_length=70)
    expiry_date = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name='get_offer_code_obj')
    is_used = models.BooleanField(default=False,blank=True,null=True)


    def __str__(self):
        return (self.profile.user.username if self.profile else "None") + "--------------"+ self.expiry_date.strftime("%d-%m-%Y")



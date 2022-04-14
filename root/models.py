from django.db import models
from django.db.models import fields
from django.db.models.fields import json
from django.utils.html import mark_safe
from root.utils import image_or_link


from root.utils import slugify

from django.core.validators import MaxValueValidator        # Validator
# Create your models here.




class Payment_options_allow(models.Model):
    Name = models.CharField(max_length=30)
    Image = models.ImageField(upload_to="root/payment_options/",null=True,blank=True)
    Image_link = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.Name
    
    def image_tag(self):
        url = image_or_link(self.Image,self.Image_link)
        return mark_safe('<img src="%s" width="90px" height="40px" />' % (url))
    
    def get_image(self):
        return image_or_link(self.Image,self.Image_link)

class delivery_label(models.Model):
    Name = models.CharField(max_length=50)
    Image = models.ImageField(upload_to="root/delivery_label/",null=True,blank=True)
    Image_link = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.Name
    
    def image_tag(self):
        url = image_or_link(self.Image,self.Image_link)
        return mark_safe('<img src="%s" width="90px" height="40px" />' % (url))



class City(models.Model):
    Name = models.CharField(max_length=50)
    Image = models.ImageField(upload_to="root/City/",null=True,blank=True)
    Image_link = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.Name
    
    def image_tag(self):
        url = image_or_link(self.Image,self.Image_link)
        return mark_safe('<img src="%s" width="90px" height="40px" />' % (url))
        
    def get_image(self):
        return image_or_link(self.Image,self.Image_link)

class Email(models.Model):
    Name = models.CharField(max_length=70)
    email = models.EmailField("Email")

    def __str__(self):
       return self.Name+" - " + str(self.email)

class Mobile(models.Model):
    Name = models.CharField(max_length=70)
    Phone = models.PositiveIntegerField(validators=[MaxValueValidator(99999999999)],verbose_name="Phone Number")

    def __str__(self):
            return self.Name+" - " + str(self.Phone)


class social_media(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="root/socal_media")
    url = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.name

class features(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="root/features")


    def __str__(self):
        return self.name  
    
from ckeditor.fields import RichTextField
# from corporate.models import Corporate
class basic_setting(models.Model):
    class Meta:
        db_table = "BASIC SETTING"
        verbose_name_plural = "BASIC ROOT SETTING"

    Name = models.CharField(max_length=100,help_text="Please Enter your website name here")
    Description = models.TextField()
    Mobile_logo = models.ImageField(upload_to="root/Others",null=True,blank=True)
    Mobile = models.ManyToManyField(Mobile,blank=True)
    Email = models.ManyToManyField(Email,blank=True)
        # socal media link
    Social_media = models.ManyToManyField(social_media,blank=True)
        # Payment Allow
  
    Payment_allow = models.ManyToManyField(Payment_options_allow,blank=True)
        # delivery options allow 
   
    delivery_allow =  models.ManyToManyField(delivery_label,blank=True)
        # App link
    Play_store = models.URLField(null=True,blank=True)
    App_store = models.URLField(null=True,blank=True)
        # Other
    allow_city = models.ManyToManyField(City,verbose_name="City",blank=True)
        #LOGO and Favicon 
    LOGO = models.ImageField(upload_to="root/Others",null=True,blank=True)
    Favicon = models.ImageField(upload_to="root/Others",null=True,blank=True)
         #Or LOGO and Favicon  with link
    LOGO_link = models.URLField(null=True,blank=True)
    Favicon_link = models.URLField(null=True,blank=True)

    Features = models.ManyToManyField(features,blank=True)
        # Reusable Bags =========================================>>>>>>>>>
    reusable_bag_price = models.PositiveIntegerField(blank=True,null=True,default=0)
    
    

    side_bar_image = models.ImageField(upload_to='root/Others',null=True,blank=True)
    
    admin_login_photo = models.ImageField(upload_to='admin/login',null=True,blank=True)
    
    Mini_Logo = models.ImageField(upload_to='admin/Others',null=True,blank=True)
    
    
    Total_sell_money = models.BigIntegerField(blank=True)
    Total_saved_money = models.BigIntegerField(blank=True)
    
    

    def __str__(self):
        return self.Name


    def get_logo(self):
        return image_or_link(self.LOGO,self.LOGO_link)

    def get_favicon(self):
        return image_or_link(self.Favicon,self.Favicon_link)
    
    def get_site_number(self):
        return "0"+ str(self.Mobile.all()[0].Phone)


Menu_type_choise =(
    ("NM","Normal Banner"),
    ("AB","App Banner")
)

class Menu(models.Model):
    class Meta:
        verbose_name_plural = "Menu's and Sub menu's"

    parent = models.PositiveIntegerField(help_text="Parent Menu id",null=True,blank=True)
    Name = models.CharField(max_length=30)
    Image = models.ImageField(upload_to="root/Menu",null=True,blank=True)
    Image_link = models.URLField(null=True,blank=True)
    Date = models.DateTimeField(auto_now_add=True,editable=True,verbose_name="Created")
    Update = models.DateTimeField(auto_now=True,editable=True,verbose_name="Last Updated")
    # ajsx
    ajsx_id = models.CharField(max_length=30,help_text="It is the id of the menu .<strong>NO SPACE ALLOW</strong>. Please require the fill or it will auto fill from Menu name slug. <i>You can give any value<i>",null=True,blank=True)

    # Record's
    page_image = models.ImageField(upload_to="root/Menu",null=True,blank=True)
    page_banner_type = models.CharField(max_length=2,choices=Menu_type_choise,null=True,blank=True,default="NM")
    
    is_use_home_menu = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.Name

    def help_text(self):
        return "Please add menu Then add submenu under the main menu"
    
    def get_image(self):
        return image_or_link(self.Image,self.Image_link)

        
    def image_tag(self):
        url = image_or_link(self.Image,self.Image_link)
        return mark_safe('<img src="%s" width="90px" height="40px" />' % (url))

    def save(self, *args, **kwargs):
        if not self.ajsx_id:
            self.ajsx_id = slugify(self.Name)

        super(Menu, self).save(*args, **kwargs)

    @property
    def has_parent(self):
         parent_id = self.parent
         if parent_id is not None:
             return True
         return False

    @property
    def has_children(self):
        children = self.__class__.objects.filter(parent=self.pk)
        if children.exists():
            return True
        return False
    

    def parent_menu(self):
            if self.has_parent:
                parent = self.parent
                parent_obj = self.__class__.objects.get(pk=parent)
                return parent_obj
            return False


    def children_menu(self):
        children = self.__class__.objects.filter(parent=self.pk)
        return children

    def total_parent(self):
        all_parent = []
        count = 0
        i = 0
        while True:
            if all_parent:
                parent = all_parent[i].parent_menu()
                if parent is False:
                    break
                all_parent.append(parent) 
                i+=1
            else:
                parent = self.parent_menu()
                if parent is False:
                    break
                all_parent.append(parent)
            count += 1
        return count



class Area(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True,related_name="get_area")

    def __str__(self):
        return f"{self.name}====>{self.city.Name}" 

        
class Delivery_Charge_record(models.Model):
    if_price = models.PositiveIntegerField()
    delivery_Charge = models.PositiveIntegerField()

    def __str__(self):
        return f"প্রাইস {self.if_price} হলে ডেলিভারি চার্জ {self.delivery_Charge} হবে"	

    

class chaldal_bottomMenu_edit(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=500,null=True,blank=True)
    need_realod = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_url(self):
        url = self.url
        if not self.need_realod:
            return url + "?matRout=True"
        return url

class chaldal_bottomMenu(models.Model):
    name = models.CharField(max_length=20,verbose_name="Menu Name")
    menu = models.ManyToManyField(chaldal_bottomMenu_edit,blank=True)

    def __str__(self):
        return self.name

class RecordOfSales(models.Model):
    year = models.IntegerField()
    sales = models.BigIntegerField()
    product = models.BigIntegerField()
    saved = models.BigIntegerField()
    order = models.BigIntegerField()
    
    def __str__(self):
        return f"{self.year} ---> {self.sales}"
    
nt_color_choices = (
    ("R","RED"),
    ("G","GREEN"),
    ("B","BLUE"),
    ("P","PINK")
)

class Notification(models.Model):
    title = models.CharField(max_length=700)
    url = models.CharField(max_length=700,null=True,blank=True)
    color = models.CharField(max_length=2,choices=nt_color_choices)
    is_new = models.BooleanField(default=True,blank=True)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.title
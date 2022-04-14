import os
from django.core.validators import FileExtensionValidator
from django.db import models
from root.models import Menu


# Create your models here.
class index_menu(models.Model):
    menu = models.OneToOneField(Menu,on_delete=models.CASCADE)
    svg = models.FileField(upload_to="index/menu_svg",validators=[FileExtensionValidator(["svg"])],default=None,null=True,blank=True)

    def __str__(self):
        return self.menu.Name
    
    def get_menu_link(self):
        return self.menu.ajsx_id
    
    def delete_img(self):
        p = self.svg.path
        if  os.path.exists(p):
            os.remove(p)
class slider_how_to_order(models.Model):
    img = models.ImageField(upload_to="index/how_to_order_slider_img/",null=True,blank=True)

    def __str__(self):
        return str(self.pk)


class why_chaldal(models.Model):
    img = models.ImageField(upload_to="index/why_chaldal_section/",null=True,blank=True)
    title = models.CharField(max_length=50)
    discription = models.CharField(max_length=200)

    def __str__(self):
            return self.title



from django.contrib import admin
from .models import *
from django.urls import path
from django.shortcuts import render ,redirect
from json import loads , dumps
# Register your models here.

class Payment_options_allow_modelClass(admin.ModelAdmin):
    list_display = ("image_tag","Name")

class delivery_label_modelClass(admin.ModelAdmin):
    list_display = ("image_tag","Name")

class City_modelClass(admin.ModelAdmin):
    list_display = ("image_tag","Name")

class Menu_modelClass(admin.ModelAdmin):
    list_display = ("image_tag","Name",'pk')
    search_fields = ['Name__icontains']

admin.site.register(basic_setting)
admin.site.register(City,City_modelClass)
admin.site.register(delivery_label,delivery_label_modelClass)
admin.site.register(Payment_options_allow,Payment_options_allow_modelClass)
admin.site.register(Email)
admin.site.register(social_media)
admin.site.register(features)
admin.site.register(Area)
admin.site.register(Mobile)
admin.site.register(Delivery_Charge_record)
admin.site.register(Menu,Menu_modelClass)
admin.site.register(chaldal_bottomMenu)
admin.site.register(chaldal_bottomMenu_edit)
admin.site.register(RecordOfSales)
admin.site.register(Notification)


admin.site.site_header = "Chaldal Administration"
admin.site.site_title = "Chaldal"

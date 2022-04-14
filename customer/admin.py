from django.contrib import admin
from .models import *
# Register your models here.
class ActiveUser_modalAdmin(admin.ModelAdmin):
    list_display=['profile','is_active']
    list_filter = ['is_active']
  


admin.site.register(Profile)
admin.site.register(user_location)
admin.site.register(user_adress)
admin.site.register(Customer_bags)
admin.site.register(Email_Verify)
admin.site.register(C8Message)
admin.site.register(ActiveUser,ActiveUser_modalAdmin)

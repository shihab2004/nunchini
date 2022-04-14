from django.contrib import admin
from .models import *
# Register your models here.
class ClientModal_admin(admin.ModelAdmin):
    list_display = ['name',"image_tag"]


admin.site.register(root)
admin.site.register(Corporate)
admin.site.register(Client,ClientModal_admin)
admin.site.register(Corporate_Customer)

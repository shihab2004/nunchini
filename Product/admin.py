from django.contrib import admin
from .models import Delivery_man, Product_image ,Product ,Order,Product_Request,Special_Code
# Register your models here.
class productModalAdmin(admin.ModelAdmin):
    search_fields = ("Name__startswith", )

class productImageModalAdmin(admin.ModelAdmin):
    search_fields = ("product__Name__icontains", )

admin.site.register(Product_image,productImageModalAdmin)
admin.site.register(Product,productModalAdmin)
admin.site.register(Order)
admin.site.register(Product_Request)
admin.site.register(Special_Code)
admin.site.register(Delivery_man)
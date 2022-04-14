from django.dispatch import receiver
from django.db.models.signals import post_save
from Product.models import Product,Order
from customer.models import Profile
from root.models import Notification, basic_setting,RecordOfSales
from support.models import ContactUs



@receiver(post_save, sender=Product)
def when_product_update(sender,instance,*args, **kwargs):
    if int(instance.Stoke_quantity or 0):
        instance.get_all_user_request.all().delete()



@receiver(post_save, sender=Order)
def when_product_update(sender,instance,created, **kwargs):
    
    
    if created:
        Notification.objects.create(
            title=f"{instance.profile} Placed A New Order",
            url=f"/admin/order/details/{instance.pk}/",
            color="G"
        )
        
    if instance.order_status == "CN":
        Notification.objects.create(
            title=f"{instance.profile} Cancelled An Order",
            url=f"/admin/order/details/{instance.pk}/",
            color="R"
        )
        
    if instance.order_status == "SF":
        year_y = instance.ordered_time.year
        year_p = Order.objects.order_by("-pk").first().ordered_time.year
        if  year_y > year_p:
            root = basic_setting.objects.get()
            RecordOfSales.objects.create(
                year= year_y,
                saved= root.Total_saved_money,
                product = Product.objects.count(),
                sales=root.Total_sell_money,
                order=Order.objects.filter(ordered_time__year=year_p).count()
            )
            
            root.Total_sell_money = 0
            root.Total_saved_money = 0
            root.save()
            
@receiver(post_save, sender=Profile)
def when_new_user_create(sender,instance,created, **kwargs):
    if created:
        Notification.objects.create(
            title=f"A New User Registration, Named {instance.user}",
            url=f"/admin/profile/{instance.pk}/",
            color="B"
        )

            
@receiver(post_save, sender=ContactUs)
def when_new_user_create(sender,instance,created, **kwargs):
    if created:
        user = f"{instance.profile.user} Send A Message" if instance.profile else "An Anonymous User Send A Message"
        Notification.objects.create(
            title=user,
            url=f"/admin/mail/details/{instance.pk}/",
            color="P"
        )




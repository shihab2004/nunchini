from django.http.response import JsonResponse
from django.shortcuts import render
from Product.views import popular
from django.urls import reverse
from .models import index_menu,why_chaldal,slider_how_to_order
from Product.models import Product ,Order
from customer.models import C8Message ,Profile
from corporate.models import Corporate , root
from root.models import basic_setting,chaldal_bottomMenu
from django.conf import settings

from math import floor
from root.utils import get_svg_text_form_file
# Create your views here.
def index(request):
    if request.GET.get('matRout'):
        context = {
            'frist_img':index_menu.objects.first().menu.page_image.url if index_menu.objects.first().menu.page_image else "",
            'second_img':index_menu.objects.all()[1].menu.page_image.url if index_menu.objects.all()[1].menu.page_image else "",
            'root':basic_setting.objects.get(),
            "corporate_image":root.objects.get().image.url,
            'how_to_order':slider_how_to_order.objects.all(),
            'ofer_order':Product.objects.filter(discord_price__gt=0,Stoke_quantity__gt=0)[0:7],
            "MEDIA_URL":settings.MEDIA_URL,
            "footer":chaldal_bottomMenu.objects.all(),
            'rated_massage':C8Message.objects.filter(is_rated=True)[0:5],
            'need_obj':False if request.GET.get('obj') or request.GET.get('popstate') else True
        }
        print(context)
        return render(request,'chaldal/index.html',context)
    elif request.GET.get('json'):

        menus = []
        for menu in index_menu.objects.all():
            menus.append({
                'name':menu.menu.Name,
                'svg':get_svg_text_form_file(menu.svg),
                "link":menu.get_menu_link()
            })


        how_to_order_slider = []
        for slide in slider_how_to_order.objects.all():
            how_to_order_slider.append({
                'img':slide.img.url
            })
        offer_products = []
        offer_obj = Product.objects.filter(discord_price__gt=0,Stoke_quantity__gt=0)[0:7]
        for i in offer_obj:
            offer_products.append({
                    "pk":i.pk,
                    "Name":i.Name,
                    "Price":i.Price,
                    "discord_price":i.get_discord_price(),
                    "Amount":i.Amount,
                    "Description":i.Description,
                    "image_link":i.product_image.get(is_main=True).get_image() if i.product_image.all() else "",
                    "slug":i.slug,
                    "is_discord_price":i.is_discord_price(),
                    'is_stoke':True if i.Stoke_quantity else False,
            })
        why_chaldal_section = []
        for i in why_chaldal.objects.all():
            why_chaldal_section.append({
                "img":i.img.url if i.img else "",
                "title":i.title,
                "discription":i.discription,
            })

        rated_message = []
        for message in C8Message.objects.filter(is_rated=True)[0:5]:
            rated_message.append({
                'name':message.profile.user.username,
                'message':message.message,
                'profile_photo':message.profile.profile_photo.url if message.profile.profile_photo else ""
            })
        corporate_section = []
        for corporate in Corporate.objects.filter(is_show_in_index_page=True):
            corporate_section.append({
                "title":corporate.title,
                "svg":get_svg_text_form_file(corporate.svg_file),
            })
        total_money_saved = 0
        for meney in Order.objects.filter(order_status="SF",discount_offer__gt=0):
            total_money_saved += float(meney.total_price(discont_price=True))

        context = {
            'status':"sucsess",
            'menu':menus,
            'how_to_order_slider':how_to_order_slider,
            'offers':offer_products,
            'why_chaldal_section':why_chaldal_section,
            'total_order':Order.objects.filter(order_status="SF").count(),
            'rated_messages':rated_message,
            'corporate_section':corporate_section,
            "total_money_saved":int(total_money_saved),
            'total_customer':Profile.objects.count()
        }

        return JsonResponse(context)

    routing_url = reverse("index")+"?matRout=True"
    return popular(request,routhing={"mat_router":routing_url})
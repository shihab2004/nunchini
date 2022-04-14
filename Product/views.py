from django.shortcuts import render
from django.http import HttpResponse
from root.models import basic_setting
from root.models import Menu,Payment_options_allow,Mobile,Email ,City , chaldal_bottomMenu
from root.utils import almost_same
from .models import Product,Product_image,Product_Request,Special_Code
from django.http import JsonResponse
from datetime import datetime



from django.urls import reverse
from django.conf import settings

# Create your views here.

def popular(request,routhing=None):
    main_menu = Menu.objects.filter(parent=None) 

    user_proifle = None
    if request.user.is_authenticated:
        user_proifle = request.user.get_profile
        crnt_city = user_proifle.current_city.Name 
    elif request.session.get('crnt_city'):
        crnt_city = City.objects.filter(pk=request.session.get('crnt_city'))[0].Name
    else:
       crnt_city = "Dhaka"
      

    #getting all offer product 
    pd_offer_count = Product.objects.filter(discord_price__gt=0)


    discout_parsent = 0
    if request.session.get('discount_code'):
        try:
            discout_parsent = Special_Code.objects.get(code=request.session.get('discount_code'),expiry_date__gte=datetime.now(),is_used=False).discount_parsent
        except Special_Code.DoesNotExist:
            del request.session['discount_code']
            


    context = {
        "root":basic_setting.objects.get(),
        "main_menu":main_menu,
        'crnt_city': crnt_city,
        'profile':user_proifle,
        "offers":pd_offer_count.count() if pd_offer_count.exists() else 0,
        "discout_parsent":discout_parsent
    }
    if routhing:
        context.update(routhing)
    else:
        context.update({"clickBaseMenu":True})
        
        
    return render(request,"chaldal/base.html",context)
   
from time import time
from django.core.paginator import Paginator
from urllib.parse import unquote
def Product_view(request,slug):

    c_time = time()
    user_profile = request.user.get_profile if request.user.is_authenticated else None


    if request.GET.get("json"):
        url = request.path.split("/")[1]
        try:
            product_menu = Menu.objects.get(ajsx_id=url)        #fetching Product ment


            if user_profile:
                user_city = user_profile.current_city
                request.session['crnt_city'] = user_city.pk
            elif request.session.get('crnt_city'):
                user_city = request.session.get('crnt_city')
            else:
                user_city = 1
                request.session['crnt_city'] = user_city
            
            
       
            item = product_menu.product.filter(city=user_city).order_by('-Stoke_quantity')                 #fetching Product of the menu
            per_page = 12
            obj_paginator = Paginator(item,per_page)

            if item.exists() and (len(obj_paginator.page_range) >= int(request.GET.get('page') or 1)):
                        product_json = {}
                        for index,i in enumerate(obj_paginator.page(request.GET.get('page') or 1).object_list):
                            if user_profile:
                                try:
                                    if user_profile.get_user_product_request.get(product__pk=i.pk):
                                        is_requested_pd = True
                                except Product_Request.DoesNotExist:
                                    is_requested_pd = False
                            else:is_requested_pd=False
                                
                            product_json_single = {
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
                                    'is_requested':is_requested_pd
                                }
                            product_json.update({index:product_json_single})
                            

                        c_time =  time() - c_time 
                       

                        return JsonResponse({"status":"succsess","product":product_json})
                        # 404 page
            return JsonResponse({"errPage":"NO PRODUCT FORND !!!"})
        except [Menu.DoesNotExist,KeyError,ValueError]:
            return JsonResponse({"errPage":"404 ERROR PAGE"})
    

    main_menu = Menu.objects.filter(parent=None)


   
    context ={
        "root":basic_setting.objects.get(),
        "menu_slug":slug,
        "main_menu":main_menu,
        "profile":user_profile,
        "isMenuClicked":True,
    
    }
 
 
    return popular(request,routhing=context)

def product_detailView(request,slug):

    product = Product.objects.get(slug=slug)
    product_image_link = []
    image_model = product.product_image.all()

    for i in image_model:
            product_image_link.append(i.get_image())

            #    CHICKING THE REQUEST is JSHON or http
    if request.GET.get("json"):
        product_context = {
            "Name":product.Name,
            "Price":product.Price,
            "discord_price":product.get_discord_price(),
            "Amount":product.Amount,
            "Description":product.Description,
            "image":product_image_link,
            "single_image":image_model.get(is_main=True).get_image(),
            "percentage_off":product.percentage_off()
        }
        return JsonResponse(product_context)
    elif request.GET.get('matRout'):

        payment_allow = Payment_options_allow.objects.all()
        
        root = basic_setting.objects.get()
        context ={
            "slug":slug,
            "product":{
                 "single_image":image_model.get(is_main=True).get_image(),
                'pk':product.pk,
                "Name":product.Name,
                "Price":product.Price,
                "discord_price":product.get_discord_price(),
                "Amount":product.Amount,
                "Description":product.Description,
                "image":product_image_link,
                "percentage_off":product.percentage_off,
                'is_stok':True if product.Stoke_quantity else False,
                'bag_qnt': request.user.get_profile.get_customerBag_item.filter(product__pk=product.pk) if request.user.is_authenticated else 0
            },
            "payment_allow":payment_allow,
            "phone":Mobile.objects.get(pk=1).Phone,
            "email":Email.objects.get(pk=1).email,
            "social_media":root.Social_media.all(),
            "Menu":Menu.objects.all(),
            "MEDIA_URL":settings.MEDIA_URL,
            "footer":chaldal_bottomMenu.objects.all()
        }
       
        context.update(almost_same(root,Menu))
        print(context)
        return render(request,"chaldal/product-detailView.html",context)
 
    
    routing_url = reverse("product:product_detail_view",kwargs={"slug":slug})+r"?matRout=True"
    return popular(request,routhing={"mat_router":routing_url})
    

def menuImageApi(request,slug):
    try:

        menu = Menu.objects.get(Name=unquote(slug)).get_image()
        return JsonResponse({"status":"succsess","img":str(menu)})
    except Menu.DoesNotExist:
        return JsonResponse({"status":"404 error","img":"No Image found"})

from django.views.decorators.cache import cache_page


def p8ModalHtml(request):
    return render(request,'chaldal/productModals.html',{'root':basic_setting.objects.get(),"MEDIA_URL":settings.MEDIA_URL,"footer":chaldal_bottomMenu.objects.all()})







def product_search(request,slug):
   
    user_city = request.session.get('crnt_city') or 1
   
   
    find_product = Product.objects.filter(Name__icontains=unquote(slug),city=user_city)

    if find_product.exists():
            product_json = {}
            for index,i in enumerate(find_product):
                    if request.user.is_authenticated:
                        try:
                            if request.user.get_profile.get_user_product_request.get(product__pk=i.pk):
                                is_requested_pd = True
                        except Product_Request.DoesNotExist:
                                is_requested_pd = False
                    else:is_requested_pd=False
                                
                    product_json_single = {
                        "pk":i.pk,
                        "Name":i.Name,
                        "Price":i.Price,
                        "discord_price":i.get_discord_price(),
                        "Amount":i.Amount,
                        "Description":i.Description,
                        "image_link":i.product_image.get(is_main=True).get_image(),
                        "slug":i.slug,
                        "is_discord_price":i.is_discord_price(),
                        'is_stoke':True if i.Stoke_quantity else False,
                        'is_requested':is_requested_pd
                    }
                    product_json.update({index:product_json_single})

            return JsonResponse({"status":"succsess","product":product_json})
    return JsonResponse({"status":"faild","data":unquote(slug)})




def Product_Offer(request):
    if request.GET.get('matRout'):
        #getting all offer product 
        return render(request,"chaldal/offer.html",{"is_nedd_obj": True if request.GET.get('obj') else None})
    elif request.GET.get('json'):
        pd_offer_count = Product.objects.filter(discord_price__gt=0,Stoke_quantity__gt=0)
        __menu = []
        __product = []
        for product in pd_offer_count:
            menu_name = product.menu.first().Name
            if not menu_name in [i.get('name') for i in __menu ]:
                __menu.append({
                    'name':product.menu.first().Name,
                    'count':product.menu.first().product.filter(discord_price__gt=0).count(),
                    'img':product.menu.first().get_image()
                })
            __product.append({
                "pk":product.pk,
                "Name":product.Name,
                "Price":product.Price,
                "discord_price":product.get_discord_price(),
                "Amount":product.Amount,
                "image_link":product.product_image.get(is_main=True).get_image() if product.product_image.all() else "",
                "slug":product.slug,
                'offer_img':product.offer_image.url if  product.offer_image else "",
                'menu_name':menu_name
            })

        
        return JsonResponse({'status':'succsess','data':{'menu':__menu,"product":__product}})

    routing_url = reverse("product:offer")+"?matRout=True&obj=True"
    return popular(request,routhing={"mat_router":routing_url})



def product_request(request):
    if request.POST:
        if request.user.is_authenticated:
            try:
                product = Product.objects.get(pk=request.POST.get('product_id'))
            except Product.DoesNotExist:
                return JsonResponse({'status':'faild',"title":"Sorry",'detail':"This product not available to us"})

            Product_Request.objects.get_or_create(profile=request.user.get_profile,product=product)
            return JsonResponse({'status':'succsess','detail':"<span style='font-weight:600; color:red'>Thanks</span> for request for the this product. We will try to bring the product in stock <span style='color:#4c8e00;font-weight:700;'>soon</span>","title":"😊"})
        return JsonResponse({'status':'faild',"title":"😐",'detail':"<span style='font-weight:700; color:red'>Sorry!!</span>. your are Not authenticated. Please Login first<br /> <a style='color:#4c8e00;font-size:15px;font-weight:700;' mat='/login/?matRout=True'>Login</a>"})




from .forms import discount_code_form
def api_api(request):
    if request.GET.get('banner_menu'):
        try:
            product_menu = Menu.objects.get(ajsx_id=request.GET.get('banner_menu'))        #fetching Product ment
        except [Menu.DoesNotExist,ValueError]:
            return HttpResponse(status=400)
        return JsonResponse({'status':'succsess','banner_type':product_menu.page_banner_type, 'image':product_menu.page_image.url if product_menu.page_image else ""})
    if request.POST:
        if request.GET.get('discountCode'):
             
                
                forms = discount_code_form(request.POST)
                if forms.is_valid():
                    try:
                       if request.user.is_authenticated:
                            obj = Special_Code.objects.get(code=request.POST.get('code'),expiry_date__gte=datetime.now(),is_used=False)
                            obj.profile = request.user.get_profile
                            request.session['discount_code'] = obj.code
                            obj.save()
                            return JsonResponse({'status':'succsess','parsent':obj.discount_parsent})
                    except Special_Code.DoesNotExist:
                        pass
        return JsonResponse({'status':'faild'})


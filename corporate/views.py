from django.shortcuts import render
from django.urls import reverse
from Product.views import popular
from django.http import JsonResponse
from .models import *
from .forms import Corporate_Customer_form
from root.models import basic_setting,chaldal_bottomMenu
from root.utils import get_svg_text_form_file
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def corporateIndex(request):
    if request.POST:
        if request.user.is_authenticated:
            post_with_profile = request.POST.copy()
            post_with_profile.update({'profile':request.user.get_profile})
        else:
            return JsonResponse({'status':"faild","title":"😶",'data':"Your are not authenticated. Please Login or sinup first🙂"})

        form = Corporate_Customer_form(post_with_profile or request.POST)
      
        if form.is_valid():
            form.save()
            return JsonResponse({'status':"successful","title":"🥰",'data':"We Recive your information. We email your soon. Thanks for joining us🥰"})
        return JsonResponse({'status':"faild","title":"😥",'data':"Your form is invalid. Please valid the form and submit again🙂"})

    if request.GET.get("matRout"):
        context ={
            'root':basic_setting.objects.get(),
            'footer_menu':chaldal_bottomMenu.objects.all()
        }
        return render(request,'chaldal/corporate/corporate.html',context)
    elif request.GET.get("json"):
        root_obj = root.objects.get()

        context = {
            "root":{
                "root_title":root_obj.title,
                'description':root_obj.description,
                'image':root_obj.image.url if root_obj.image else "" ,
                'email':root_obj.email.email,
                "mobile":root_obj.mobile.Phone
            },
            'corporates':[],
            'clients':[]
        }

        try:
            if request.user.is_authenticated:
                corporate_customer = request.user.get_profile.get_corporate_customer
                context.update({"corporate_customer":{
                    'Business_Name':corporate_customer.Business_Name,
                    "Phone_Number":corporate_customer.Phone_Number,
                    "Representative_Name":corporate_customer.Representative_Name,
                    "Email_Address":corporate_customer.Email_Address,
                }})

        except ObjectDoesNotExist:
            corporate_customer = None
       
        for i in Corporate.objects.all():
            context['corporates'].append({
                "title":i.title,
                "description":i.description,
                "svg":get_svg_text_form_file(i.svg_file),
            })
        for i in Client.objects.all():
            context['clients'].append({
                "name":i.name,
                "image":i.image.url if i.image else "",
            })
        return JsonResponse({'status':"successful",'data':context})

    routing_url = reverse("corporate:index")+"?matRout=True"
    return popular(request,routhing={"mat_router":routing_url})


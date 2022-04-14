
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from corporate.models import Client, Corporate, Corporate_Customer
from index.models import index_menu
from root.models import Area, Email, Notification, RecordOfSales, basic_setting,City,Menu, chaldal_bottomMenu, chaldal_bottomMenu_edit, features
from root.forms import AuthForm
from django.contrib.auth import authenticate , login
from customer.models import ActiveUser, C8Message, Profile
from Product.models import Delivery_man, Order ,Product, Product_Request, Product_image, Special_Code
from root.views import error_404
from support.models import ContactUs, Team, support_menu

from datetime import date
from root.utils import super_user_required
# Create your views here.

def login_admin(request):
    if request.POST:
         authForms = AuthForm(request.POST)


         if authForms.is_valid():
            user_model = authenticate(username=authForms.cleaned_data['username'],password=authForms.cleaned_data['password'])
            if user_model:

                login(request,user_model)

            return HttpResponseRedirect(reverse("ADMIN:admin_home"))

    root = basic_setting.objects.get()
    contex = {
        "name":root.Name,
        "img":root.admin_login_photo.url
    }

    return render(request,"admin/Login/index.html",contex)



# /////////////////////////////////////////////////////////////




from .helper import order_yearly_chart_report, sealize_time

def Home(request):
    if request.user.is_authenticated and request.user.is_superuser:

        root = basic_setting.objects.get()

        total_sales = 0
        sales_record = RecordOfSales.objects.all()
        for i in sales_record:
            total_sales = total_sales + i.sales

        total_sales = total_sales + root.Total_sell_money


        #this year order status code
        this_year_order = Order.objects.filter(ordered_time__year=date.today().year).count()

        suc_order = Order.objects.filter(ordered_time__year=date.today().year,order_status="SF").count()
        ps_order = Order.objects.filter(ordered_time__year=date.today().year,order_status="PS").count()
        pn_order = Order.objects.filter(ordered_time__year=date.today().year,order_status="PN").count()
        cn_order = Order.objects.filter(ordered_time__year=date.today().year,order_status="CN").count()


        this_year_order_status_dic = {
            "per_suc_order":"%.2f" % ((suc_order / this_year_order) *100) if this_year_order else 0,
            "per_ps_order":"%.2f" % ((ps_order / this_year_order) *100) if this_year_order else 0,
            "per_pn_order":"%.2f" % ((pn_order / this_year_order) *100) if this_year_order else 0,
            "per_cn_order":"%.2f" % ((cn_order / this_year_order) *100) if this_year_order else 0,
        }


        #today order status
        this_month_order = Order.objects.filter(ordered_time__year=date.today().year,ordered_time__month=date.today().month).count()

        month_order_status = {
            "per_suc_order": "%.2f" % ((Order.objects.filter(ordered_time__year=date.today().year,ordered_time__month=date.today().month,order_status="SF").count() / this_month_order) * 100) if this_month_order else 0,
            "per_ps_order": "%.2f" % ((Order.objects.filter(ordered_time__year=date.today().year,ordered_time__month=date.today().month,order_status="PS").count() / this_month_order) * 100) if this_month_order else 0,
            "per_pn_order": "%.2f" % ((Order.objects.filter(ordered_time__year=date.today().year,ordered_time__month=date.today().month,order_status="PN").count() / this_month_order) * 100) if this_month_order else 0,
            "per_cn_order": "%.2f" % ((Order.objects.filter(ordered_time__year=date.today().year,ordered_time__month=date.today().month,order_status="CN").count() / this_month_order) * 100) if this_month_order else 0,
        }



        mails = ContactUs.objects.filter(status="N").order_by("-pk")[0:5]
        if not mails:
            mails = ContactUs.objects.all().order_by("-pk")[0:5]

        context = {
            'new_corporate_req':Corporate_Customer.objects.filter(is_view=False).count(),
            "mails":mails,
            "demo_order_list":Order.objects.all().order_by('-pk')[0:5],
            'this_year_order_status':this_year_order_status_dic,
            "month_order_status":month_order_status,
            'sales_record':sales_record,
            "total_sales":total_sales,
            'copyRight':date.today().year,
            "profile":request.user.get_profile,
            "root":root,
            "total_user":Profile.objects.count(),
            "Pending_order":Order.objects.filter(order_status="PN").count(),
            "success_order":Order.objects.filter(order_status="SF").count(),
            "total_product": Product.objects.count(),
            "Processing_orders":Order.objects.filter(order_status="PS").count(),
            "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
            "new_mail":ContactUs.objects.filter(status="N").count(),
            "order_yearly_report_Suc":order_yearly_chart_report(date.today().year,status="SF"),
            "order_yearly_report_Cen":order_yearly_chart_report(date.today().year,status="CN")
        }

        return render(request,"admin/home/index.html",context)
    return HttpResponseRedirect(reverse("ADMIN:login_admin"))



from django.core.paginator import Paginator
@super_user_required
def admin_order_list(request):
    if request.GET.get('search'):
        ooo = Order.objects.filter(pk=request.GET.get('search'))
    else:
        ooo = Order.objects.all().order_by("-pk")

    obj_paginator = Paginator(ooo,16)


    list_of_next_page = []

    cc_page  = request.GET.get("page") if request.GET.get("page") else 1
    for i in range(int(cc_page),int(cc_page) + 7):

        if i < obj_paginator.num_pages + 1:
            list_of_next_page.append(i)
        else:
            break


    contex = {
        "count":Order.objects.count(),
         "new_mail":ContactUs.objects.filter(status="N").count(),
            "order":obj_paginator.get_page(cc_page),
            'page_range':range(1,obj_paginator.num_pages + 1),
            "c_page":int(cc_page),
            "list_of_next_page":list_of_next_page,
            "p_page":int(cc_page) - 1 if int(cc_page) else 1,
            "n_page":int(cc_page) + 1 if int(cc_page) else 1,
            "is_last_page":int(cc_page) == obj_paginator.num_pages ,
            "profile":request.user.get_profile,
            "root":basic_setting.objects.get(),
            'copyRight':date.today().year,
            "current_page":int(cc_page),
            "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }



    return render(request,"admin/home/order_list.html",contex)





@super_user_required
def admin_order_details(request,pk):
    if request.GET.get('notifation'):
         Notification.objects.filter(pk=request.GET.get('id')).update(is_new=False)

    root = basic_setting.objects.get()
    orderObj = Order.objects.get(pk=pk)
    if request.method == "POST":

        status = request.POST.get("status")

        if status == "CN":
            root.Total_sell_money = root.Total_sell_money - float(orderObj.total_price())
            if orderObj.discount_offer:
                root.Total_saved_money = root.Total_saved_money - float(orderObj.total_price(True))
                root.save()


        if status == "SF":
            root.Total_sell_money = root.Total_sell_money + float(orderObj.total_price())
            if orderObj.discount_offer:
                root.Total_saved_money = root.Total_saved_money + float(orderObj.total_price(True))
                root.save()

        orderObj.delivery_man = Delivery_man.objects.get(pk=request.POST.get('dvm'))
        orderObj.order_status = status
        orderObj.save()



    contex = {
            "order":orderObj,
            "new_mail":ContactUs.objects.filter(status="N").count(),
            "profile":request.user.get_profile,
            "root":root,
            'copyRight':date.today().year,
             "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
            "dvms":Delivery_man.objects.all()
    }
    return render(request,"admin/home/order_list_details.html",contex)





@super_user_required
def admin_product_list(request):

    contex = {
         "new_mail":ContactUs.objects.filter(status="N").count(),
            "prod":Product.objects.all(),
            "profile":request.user.get_profile,
            "root":basic_setting.objects.get(),
            'copyRight':date.today().year,
            "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }

    return render(request,"admin/home/product_list.html",contex)

import json
@super_user_required
def admin_product_list_details(request,pk):
    if request.method == "POST":
        post = request.POST




        a = Product.objects.get(pk=pk)
        a.Name = post.get("Name")
        a.Price = post.get("price")
        a.discord_price = post.get("discord_price")
        a.Amount = post.get("Amount")
        a.Description = post.get("Description")
        a.Stoke_quantity = post.get("Stoke_quantity")

        if request.FILES.get("product_image"):
             a.product_image.create(
            product = a,
            image = request.FILES.get('product_image')
            )
        if request.FILES.get("product_image_offer"):
            a.offer_image = request.FILES.get("product_image_offer")



        if post.get("checkImage"):
           b = a.product_image.get(is_main=True)
           b.is_main = False
           b.save()
           a.product_image.filter(pk=post.get("checkImage")).update(is_main=True)


        a.menu.clear()
        a.city.clear()


        for i in post.get('menu').split(","):
             a.menu.add(i)

        for i in post.get('city').split(","):
            a.city.add(i)
        a.save()


    try:
        prod = Product.objects.get(pk=pk)

        cy = []
        for i in prod.city.all():
            cy.append(i.Name)
        my = []
        for i in prod.menu.all():
            my.append(i.Name)

        contex = {
             "new_mail":ContactUs.objects.filter(status="N").count(),
            "heading":f"#{prod.id} Product Details",
            'city':City.objects.all(),
            'main_img':prod.product_image.get(is_main=True).get_image(),
            "product":prod,
            "my":my,
            'cy':cy,
            "profile":request.user.get_profile,
            'copyRight':date.today().year,
            "root":basic_setting.objects.get(),
            'menu':Menu.objects.all(),
            "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],

        }
        return render(request,"admin/home/product_list_details.html",contex)

    except Exception as e:
      print(e)
      return error_404(request)

@super_user_required
def admin_product_create(request):

    if request.method == "POST":
        post = request.POST
        a = Product.objects.create(
        Name = post.get("Name"),
        Price = post.get("price"),
        discord_price = post.get("discord_price"),
        Amount = post.get("Amount"),
        Description = post.get("Description"),
        Stoke_quantity = post.get("Stoke_quantity"),
        )
        print(a)
        print(request.FILES)
        if request.FILES.get("product_image"):
             a.product_image.create(
            product = a,
            image = request.FILES.get('product_image'),
            is_main=True
            )

        for i in post.get('menu').split(","):
             a.menu.add(i)

        for i in post.get('city').split(","):
            a.city.add(i)
        a.save()

        if request.FILES.get("product_image_offer"):
            a.offer_image = request.FILES.get("product_image_offer")

    contex = {
         "new_mail":ContactUs.objects.filter(status="N").count(),
        "heading":"Create New Product",
        'city':City.objects.all(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        'menu':Menu.objects.all(),
        "create": "a",
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/product_list_details.html",contex)

@super_user_required
def admin_product_delete(request,pk):
    Product.objects.filter(pk=pk).delete()

    return  HttpResponseRedirect(reverse("ADMIN:admin_product_list"))

@super_user_required
def mail(request):
    obj_paginator = Paginator(ContactUs.objects.all().order_by("-pk"),12)


    contex = {
        "new_mail":ContactUs.objects.filter(status="N").count(),
        'page_range':range(1,obj_paginator.num_pages + 1),
        "mail":obj_paginator.get_page(request.GET.get('page') or 1),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "current_page":int(request.GET.get('page') or 1),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/mail.html",contex)

@super_user_required
def mail_details(request,pk):
    if request.GET.get('notifation'):
        Notification.objects.filter(pk=request.GET.get('id')).update(is_new=False)

    cc = ContactUs.objects.get(pk=pk)

    if cc.status == "N":
        cc.status = "Y"
        cc.save()

    contex = {
        'mail':cc,
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/mail_details.html",contex)





#Menu
@super_user_required
def product_menu(request):
    contex = {
        "menu":Menu.objects.all().order_by("-pk"),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }

    return render(request,"admin/home/product_menu.html",contex)

@super_user_required
def product_menu_create(request):
    if request.method == "POST":
        post = request.POST


        print(request.FILES)
        Menu.objects.create(
           parent=post.get("parent_menu") if post.get("parent_menu") != "0" else None,
            Name=post.get("Name"),
            Image=request.FILES.get("menu_img"),
            page_image= request.FILES.get("banner_img"),
            page_banner_type=post.get("banner_type"),
        )
        return redirect("ADMIN:product_menu")

    contex = {
         "menu":Menu.objects.all(),
        'is_dt':False,
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }

    return render(request,"admin/home/product_menu_cud.html",contex)



@super_user_required
def product_menu_details(request,pk):
    c = Menu.objects.filter(pk=pk)

    if request.method == "POST":
        post = request.POST
        f = c.first().Image if c.first().Image else None
        l = c.first().page_image if c.first().page_image else None
        if request.FILES.get("menu_img"):
            f = request.FILES.get("menu_img")

        if request.FILES.get("banner_img"):
            l = request.FILES.get("banner_img")

        print(request.FILES.get('menu_img'))

        d = c.first()


        d.parent = post.get("parent_menu") if post.get("parent_menu") != "0" else None
        d.Image = f
        d.Name=post.get("Name")
        d.page_image=  l
        d.page_banner_type= post.get("banner_type")

        d.save()

    contex = {
        "c_menu":c.first(),
        "menu":Menu.objects.all(),
        'is_dt':True,
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "heading":f"Update #{c.first().id} Menu",
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/product_menu_cud.html",contex)

@super_user_required
def product_menu_delete(request,pk):
    Menu.objects.filter(pk=pk).delete()
    return redirect("ADMIN:product_menu")










@super_user_required
def home_menu(request):
    contex = {
        "menu":index_menu.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/home_menu.html",contex)

@super_user_required
def home_menu_create(request):
    if request.method == "POST":
        post = request.POST
        m = Menu.objects.get(pk=post.get("Name"))
        m.is_use_home_menu = True
        m.save()
        index_menu.objects.create(
            menu=m,
            svg=request.FILES.get("svg")
        )
        return redirect("ADMIN:home_menu")




    contex = {
        "heading":"Create New Home Menu",
        "menu":Menu.objects.exclude(is_use_home_menu=True),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/home_menu_cud.html",contex)

@super_user_required
def home_menu_details(request,pk):
    m = index_menu.objects.get(pk=pk)

    if request.method == "POST":
        post = request.POST
        m2 = Menu.objects.get(pk=post.get("Name"))


        m3 = m.menu
        m3.is_use_home_menu = False
        m3.save()

        m.menu = m2
        m2.is_use_home_menu = True
        m2.save()




        if request.FILES.get("svg"):
            m.svg = request.FILES.get("svg")
        m.save()
        return redirect("ADMIN:home_menu")

    contex = {
        "is_dt":True,
        "c_menu":m,
        "heading":f"Edit #{m.menu.id} Home Menu",
        "menu":Menu.objects.exclude(is_use_home_menu=True),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/home_menu_cud.html",contex)

@super_user_required
def home_menu_delete(request,pk):
    a = index_menu.objects.get(pk=pk)
    a.menu.is_use_home_menu = False
    a.menu.save()
    a.delete_img()
    a.delete()
    return redirect("ADMIN:home_menu")









@super_user_required
def help_more_menu(request):
    contex = {
        "menu":support_menu.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/help_more_menu.html",contex)

@super_user_required
def help_more_create(request):
    if request.method == "POST":
        post = request.POST
        print(post)
        support_menu.objects.create(
            name=post.get('Name'),
            img=request.FILES.get('img'),
            body=post.get('Description')
        )

    contex = {
        "heading":"Create Support Menu",
        "menu":support_menu.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/help_more_cud.html",contex)


@super_user_required
def help_more_details(request,pk):
    c_menu = support_menu.objects.get(pk=pk)
    if request.method == "POST":
        post = request.POST
        c_menu.name  =post.get('Name')
        if request.FILES.get('img'):

            img = request.FILES.get('img')

        c_menu.body = post.get('Description')

        c_menu.save()

    contex = {
        "is_dt":True,
        "heading":f"Change #{c_menu.id} Support Menu",
        "c_menu":c_menu,
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/help_more_cud.html",contex)


@super_user_required
def help_more_delete(request,pk):
    support_menu.objects.get(pk=pk).delete()
    return redirect("ADMIN:help_more_menu")











@super_user_required
def footer_menu(request):
    contex = {
        "menu":chaldal_bottomMenu.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/footer_menu.html",contex)

@super_user_required
def footer_menu_create(request):
    if request.method == "POST":
        post = request.POST
        a = chaldal_bottomMenu.objects.create(
            name = post.get("Name")
        )


        for i in post.get("subMenu"):

            a.menu.add(i)

        a.save()

        return redirect("ADMIN:footer_menu")

    contex = {
        "sub_menu":chaldal_bottomMenu_edit.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
        "root":basic_setting.objects.get(),
    }
    return render(request,"admin/home/footer_menu_cud.html",contex)

from json import loads
@super_user_required
def footer_menu_details(request,pk):
    menu = chaldal_bottomMenu.objects.get(pk=pk)
    if request.method == "POST":

        post = loads(request.POST.get('obj'))

        menu.menu.clear()
        menu.name = post.get("name")
        for i in post.get("subMenu"):

            menu.menu.add(i)

        menu.save()

    contex = {
        "is_dt":True,
        "heading":f"Update ({menu.name}) Footer Menu",
        "menu":menu,
        "sub_menu":chaldal_bottomMenu_edit.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/footer_menu_cud.html",contex)

@super_user_required
def footer_menu_delete(request,pk):
    chaldal_bottomMenu.objects.get(pk=pk).delete()
    return redirect("ADMIN:footer_menu")




@super_user_required
def footer_menuSub(request):
    contex = {
        "is_sub":True,
        "menu":chaldal_bottomMenu_edit.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/footer_menu.html",contex)

@super_user_required
def footer_menuSub_create(request):

    if request.method == "POST":
        post = request.POST
        chaldal_bottomMenu_edit.objects.create(name=post.get("Name"),url=post.get('url'))
        return redirect("ADMIN:footer_menuSub")

    contex = {
        "heading":"Create Footer Sub Menu",
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/footer_menuSub_cud.html",contex)


@super_user_required
def footer_menuSub_details(request,pk):
    menu = chaldal_bottomMenu_edit.objects.get(pk=pk)

    if request.method == "POST":
        post = request.POST
        menu.name = post.get("Name")
        menu.url=post.get('url')
        menu.save()
        return redirect("ADMIN:footer_menuSub")

    contex = {
        'is_dt':True,
        "heading":f"Update {menu.name} Footer Sub Menu",
        "menu":menu,
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/footer_menuSub_cud.html",contex)


@super_user_required
def footer_menuSub_delete(request,pk):
    chaldal_bottomMenu_edit.objects.get(pk=pk).delete()
    return redirect("ADMIN:footer_menuSub")








#root
@super_user_required
def admin_root(request):
    root = basic_setting.objects.get()
    if request.method == "POST":
        post = request.POST
        file = request.FILES
        if request.GET.get("SS"):
            post = loads(post.get('obj'))
            root.Name = post.get("name")
            root.Description = post.get("dis")
            root.Email.clear()
            for i in post.get('subMenu'):
                root.Email.add(i)

            root.save()


        elif request.GET.get("CDI"):
            if file.get('logo'):
                root.LOGO = file.get('logo')
                root.save()

            if file.get('favicon'):
                root.Favicon = file.get('favicon')
                root.save()

            if file.get('mini_logo'):
                root.Mini_Logo = file.get('mini_logo')
                root.save()

            if file.get('login_img'):
                root.admin_login_photo = file.get('login_img')
                root.save()


        elif request.GET.get("OS"):
            root.reusable_bag_price =  post.get('reusable_bag_price')
            if file.get("side_bar_image"):
                root.side_bar_image = file.get("side_bar_image")
            root.save()

        elif request.GET.get("emedit"):
            Email.objects.filter(pk=post.get("eid")).update(Name=post.get("namesh"),email=post.get("emailsh"))

        elif request.GET.get("ecreate"):
            Email.objects.create(Name=post.get("namesh"),email=post.get("emailsh"))

    contex = {
        "mail":Email.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":root,
        "mobile":Email.objects.all(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/root.html",contex)

@super_user_required
def delete_mobile(request,pk):
    Email.objects.get(pk=pk).delete()
    return redirect("ADMIN:admin_root")

@super_user_required
def delivery_man12(request):

    contex = {
        "obj":Delivery_man.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/delivery_man_list.html",contex)


@super_user_required
def delivery_man12_create(request):
    if request.method == "POST":
        Delivery_man.objects.create(
            name=request.POST.get("name"),
            photo=request.FILES.get('photo')
        )
        return redirect("ADMIN:delivery_man")
    contex = {
        "heading":"Create Delivery Man",
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/delivery_man12_cud.html",contex)


@super_user_required
def delivery_man12_update(request,pk):
    d = Delivery_man.objects.get(pk=pk)
    if request.method == "POST":
        d.name =  request.POST.get('name')
        if request.FILES.get('photo'):
            d.photo = request.FILES.get('photo')
        d.save()
        return redirect("ADMIN:delivery_man")

    contex = {
        "heading":f"Change {d.name} Delivery Profile",
        "is_dt":True,
        "obj":d,
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/delivery_man12_cud.html",contex)


@super_user_required
def delivery_man12_delete(request,pk):
    Delivery_man.objects.get(pk=pk).delete()
    return redirect("ADMIN:delivery_man")




#Bsiness Code
@super_user_required
def business_client(request):
    contex = {
        'obj':Client.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/busness_client.html",contex)

@super_user_required
def business_corporate(request):
    post = request.POST
    get = request.GET
    obj = None
    heading = ""
    if get.get('editing'):
        parameters = ""
        dt = False
        file = request.FILES
        if get.get('update'):
            dt = True
            obj = Corporate.objects.get(pk=get.get('update'))
            parameters = f"?editing=True&update={obj.pk}"
            heading = f"Change {obj.title} Corporate"

            if request.method == "POST":
                obj.title = post.get('Name')
                if file.get("img"):
                    obj.svg_file = file.get('img')
                obj.description = post.get('Description')
                obj.is_show_in_index_page = True if post.get('is_index') == "true" else False
                obj.save()

        elif get.get('create'):
            heading = "Create Corporate"
            parameters = "?editing=True&create=True"
            if request.method == "POST":
                Corporate.objects.create(
                    title = post.get('Name'),
                    description=post.get('Description'),
                    svg_file=file.get('img'),
                    is_show_in_index_page=True if post.get('is_index') == "true" else False
                )
        elif get.get('delete'):

            Corporate.objects.get(pk=get.get('delete')).delete()
            return redirect("ADMIN:business_corporate")


        contex = {
            'submit_keyword':parameters,
            "is_dt":dt,
            "heading":heading,
            'obj':obj,
            "new_mail":ContactUs.objects.filter(status="N").count(),
            "profile":request.user.get_profile,
            'copyRight':date.today().year,
            "root":basic_setting.objects.get(),
            "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
        }
        return render(request,"admin/home/busness_corporate_cud.html",contex)

    contex = {
        'obj':Corporate.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/busness_corporate.html",contex)




@super_user_required
def business_request(request):
    contex = {
        'new_c_r':Corporate_Customer.objects.filter(is_view=False).count(),
        'obj':Corporate_Customer.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/busness_corporate_request.html",contex)

@super_user_required
def business_request_view(request,pk):
    onj = Corporate_Customer.objects.get(pk=pk)
    onj.is_view = True
    onj.save()
    contex = {
        'obj':onj,
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/busness_corporate_request_view.html",contex)





#Other menu
@super_user_required
def d_feature(request):
    file = request.FILES
    post = request.POST
    get = request.GET
    root = basic_setting.objects.get()

    contex = {
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":root,
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }

    if get.get('editing'):



        if get.get('create'):

            if request.method == "POST":
                a = features.objects.create(
                    name=post.get('name'),
                    image=file.get('img')
                )

                root.Features.add(a)
                root.save()
                return redirect("ADMIN:d_feature")

            contex.update({
                'heading':"Create Site Delivery Feature",
                "acUrl":"?editing=True&create=True"
            })
            return render(request,"admin/home/feather_cud.html",contex)

        elif get.get('view'):
            obj = features.objects.get(pk=get.get('view'))
            if request.method == "POST":
                obj.name = post.get('name')
                if file.get('img'):
                    obj.image = file.get('img')
                obj.save()
                return redirect("ADMIN:d_feature")
            contex.update({
                'ac_to_R':f"?editing=True&delete=True",
                'is_dt':True,
                'obj':obj,
                'heading':f"Change ({obj.name}) Site Delivery Feature",
                "acUrl":f"?editing=True&view={obj.pk}"
            })
            return render(request,"admin/home/feather_cud.html",contex)

        elif get.get('delete'):
            if request.method == 'POST':
                features.objects.get(pk=post.get('id')).delete()
                return redirect("ADMIN:d_feature")



    contex.update({
         'obj':features.objects.all(),
    })

    return render(request,"admin/home/feather.html",contex)

@super_user_required
def user_profile(request,pk):
    u_profile = Profile.objects.get(pk=pk)

    if request.method == "POST":

        u_profile.user.is_superuser = True if request.POST.get("is_su") else False
        u_profile.user.save()


    if request.GET.get('notifation'):
        Notification.objects.filter(pk=request.GET.get('id')).update(is_new=False)



    contex = {
        'obj':u_profile,
        "order_suc":u_profile.get_user_order.filter(order_status="SF"),
        "order_cen":u_profile.get_user_order.filter(order_status="CN"),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
            "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }

    return render(request,"admin/home/profile.html",contex)

@super_user_required
def notification_view(request):

    obj_paginator = Paginator(Notification.objects.all(),12)

    contex = {
        'page_range':range(1,obj_paginator.num_pages + 1),
        "obj":obj_paginator.get_page(request.GET.get('page') or 1),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
        "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }

    return render(request,"admin/home/notification.html",contex)

from django.template.loader import get_template
# from xhtml2pdf import pisa
@super_user_required
def admin_order_pdf(request,pk):
    return render(request,"admin/home/pdf.html",{"o":Order.objects.get(pk=pk)})

@super_user_required
def p_request(request):
    contex = {
        'obj':Product_Request.objects.all(),
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
        "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    return render(request,"admin/home/p_request.html",contex)



@super_user_required
def city_view(request):
    contex = {
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
        "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }



    get = request.GET

    if get.get('editing'):
        post = request.POST
        file = request.FILES
        method = request.method

        if get.get('create'):
            if method == "POST":
                City.objects.create(Name=post.get('name'),Image=file.get('img'))
                return redirect("ADMIN:city_view")

            contex.update({
                'heading':"Create New City",
                "acUrl":"?editing=True&create=True"
            })

        if get.get('update'):
            obj = City.objects.get(pk=get.get('update'))

            if method == "POST":
                obj.Name = post.get('name')
                if file.get('img'):
                    obj.Image = file.get('img')

                obj.save()

                return redirect("ADMIN:city_view")

            contex.update({
                'is_dt':True,
                'heading':f"Update {obj.Name} City",
                "acUrl":f"?editing=True&update={obj.pk}",
                "obj":obj,
                "ac_to_R":"?editing=True&delete=True"
            })

        if get.get('delete'):
            if method == "POST":
                City.objects.get(pk=post.get('id')).delete()
                return redirect("ADMIN:city_view")

        return render(request,"admin/home/city_cud.html",contex)




    contex.update({
        'obj':City.objects.all(),
    })
    return render(request,"admin/home/city_view.html",contex)

@super_user_required
def area_view(request):
    contex = {
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
        "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }


    contex.update({
        'obj':Area.objects.all()
    })

    get = request.GET

    if get.get('editing'):
        post = request.POST
        file = request.FILES
        method = request.method

        if get.get('create'):
            if method == "POST":
                Area.objects.create(name=post.get('name'),city=City.objects.get(pk=post.get('city')))
                return redirect("ADMIN:area_view")

            contex.update({
                'heading':"Create New Area",
                "acUrl":"?editing=True&create=True",
                "city_all":City.objects.all()
            })

        if get.get('update'):
            obj = Area.objects.get(pk=get.get('update'))

            if method == "POST":
                obj.name = post.get('name')
                obj.city = City.objects.get(pk=post.get('city'))

                obj.save()

                return redirect("ADMIN:area_view")

            contex.update({
                'is_dt':True,
                'heading':f"Update {obj.name} Area",
                "acUrl":f"?editing=True&update={obj.pk}",
                "obj":obj,
                "ac_to_R":"?editing=True&delete=True",
                "city_all":City.objects.all()
            })

        if get.get('delete'):
            if method == "POST":
                Area.objects.get(pk=post.get('id')).delete()
                return redirect("ADMIN:area_view")

        return render(request,"admin/home/area_cud.html",contex)


    return render(request,"admin/home/area_view.html",contex)


@super_user_required
def team(request):

    get = request.GET
    contex = {
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
        "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }


    if get.get('editing'):
        post = request.POST
        file = request.FILES
        method = request.method

        if get.get('create'):
            if method == "POST":
                Team.objects.create(name=post.get('name'),occupation=post.get('job'),photo=file.get('img'),discription=post.get('Description'))
                return redirect("ADMIN:area_view")

            contex.update({
                'heading':"Add New Member",
                "acUrl":"?editing=True&create=True",
            })

        if get.get('update'):
            obj = Team.objects.get(pk=get.get('update'))

            if method == "POST":
                obj.name = post.get('name')
                obj.occupation = post.get('job')
                obj.discription = post.get('Description')

                if file.get('img'):
                    obj.photo = file.get('img')


                obj.save()


            contex.update({
                'is_dt':True,
                'heading':f"Update {obj.name} info",
                "acUrl":f"?editing=True&update={obj.pk}",
                "obj":obj,
                "ac_to_R":"?editing=True&delete=True",
            })

        if get.get('delete'):
            if method == "POST":
                Team.objects.get(pk=post.get('id')).delete()
                return redirect("ADMIN:team")

        return render(request,"admin/home/team_cud.html",contex)


    contex.update({
        "obj":Team.objects.all().order_by('-pk')
    })

    return render(request,"admin/home/team.html",contex)



@super_user_required
def offer_code(request):
    contex = {
        "new_mail":ContactUs.objects.filter(status="N").count(),
        "profile":request.user.get_profile,
        'copyRight':date.today().year,
        "root":basic_setting.objects.get(),
        "new_notication_count":Notification.objects.filter(is_new=True).count(),
        "new_notication":Notification.objects.filter(is_new=True).order_by('-pk')[0:5],
    }
    get = request.GET
    if get.get('editing'):
        post = request.POST
        method = request.method

        if get.get('create'):
            if method == "POST":
                Special_Code.objects.create(
                    discount_parsent= post.get('dp'),
                    code=post.get('code'),
                    expiry_date=sealize_time(post.get('ex_date'))
                )
                return redirect("ADMIN:offer_code")

            contex.update({
                'heading':"Add  ",
                "acUrl":"?editing=True&create=True",
            })




        if get.get('update'):
            obj = Special_Code.objects.get(pk=get.get('update'))

            if method == "POST":
                obj.discount_parsent = post.get('dp')
                obj.code = post.get('code')

                obj.expiry_date = sealize_time(post.get('ex_date'))

                obj.save()

                return redirect("ADMIN:offer_code")


            contex.update({
                'is_dt':True,
                'heading':f"Update #{obj.id} Special Code",
                "acUrl":f"?editing=True&update={obj.pk}",
                "obj":obj,
                "ac_to_R":"?editing=True&delete=True",
            })





        if get.get('delete'):
            if method == "POST":
                Special_Code.objects.get(pk=post.get('id')).delete()
                return redirect("ADMIN:offer_code")

        return render(request,"admin/home/offer_code_cud.html",contex)



    contex.update({
        "obj":Special_Code.objects.all()
    })
    return render(request,"admin/home/offer_code.html",contex)












from django.forms import utils
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from root.utils import almost_same
from root.models import Menu,basic_setting,City,Area,Delivery_Charge_record
from customer.models import Customer_bags,Email_Verify
from Product.models import Product ,Order ,report_choise,Special_Code
from .models import Profile ,user_adress
from django.http import JsonResponse
from json import dumps, loads

from .forms import gender_from , order_report_form ,order_star_submit
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.utils.timezone import now
import datetime
# Create your views here.

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from time import time

def profile(request):
    # user = Profile.objects.select_related("user").get(user=request.user)
                                        # OR
    user = request.user.get_profile
    root =  basic_setting.objects.get()
    print("###############################################")
    city = root.allow_city.all()


    if request.user.is_authenticated:
        user_proifle = request.user.get_profile
        crnt_city = user_proifle.current_city.Name
    elif request.session.get('crnt_city'):
        crnt_city = City.objects.filter(pk=request.session.get('crnt_city'))[0].Name
    else:
       crnt_city = "Dhaka"


    discout_parsent = 0
    if request.session.get('discount_code'):
        try:
            discout_parsent = Special_Code.objects.get(code=request.session.get('discount_code'),expiry_date__gte=datetime.datetime.now(),is_used=False).discount_parsent
        except Special_Code.DoesNotExist:
            del request.session['discount_code']


    pd_offer_count = Product.objects.filter(discord_price__gt=0)
    context={
        "profile":user,
        "city":city,
        "POST_API":reverse("customer:post_data"),
        "is_geo":user.is_geoLocation(),
        "crnt_city":crnt_city,
        "offers":pd_offer_count.count() if pd_offer_count.exists() else 0,
        "discout_parsent":discout_parsent
    }
    context.update(almost_same(basic_setting.objects.get(),Menu))
    return render(request,"chaldal/customer/profile.html",context)

from customer.forms import profile_update_form
from re import findall
from django.template import Template , Context
def post_data2(request):
    post = request.POST
    if post:
        get = request.GET
        if get.get("update_profile"):
            forms = profile_update_form(post,request.FILES)
            if forms.is_valid():
                if request.user.is_authenticated:
                    request.user.get_profile.profile_photo = forms.cleaned_data['profile_photo']
                    request.user.get_profile.save()

                    return JsonResponse({"state":"successful",'data':"Your profile successful updated"})
                return JsonResponse({"state":"err",'data':"Your are not authenticated🙂.Please login first!"})
            return JsonResponse({"state":"err",'data':"File error. Update the right extension formet file🙂"})


        elif get.get("update_current_city"):
            try:
                city = City.objects.get(pk=post["current_city"])
                if request.user.is_authenticated:
                    request.user.get_profile.current_city = city
                    request.user.get_profile.save()


                request.session['crnt_city'] = city.pk
                return JsonResponse({"state":"successful","city":city.Name})
            except City.DoesNotExist:
                return JsonResponse({"err":"403 forbiden"},status=403)

        elif get.get('cancelOrder'):
            user_profile = request.user.get_profile

            try:
                order_id = loads(post['data'])['orderId']
                order_obj = user_profile.get_user_order.filter(pk=order_id)
                if order_obj.exists():
                    order_obj.update(
                        order_status="CN"
                    )
                    routing_url = reverse("customer:payment")+f"?matRout=True&orderId={order_obj.first().pk}"
                    return JsonResponse({"status":"successful","matRout":routing_url,"isLocalSessionclear":True})
            except ValueError:
                pass
            return HttpResponseBadRequest("Bad request No order Found!!!")

        elif get.get('email_varify'):
            print(post.get('email'))
            test_str = findall(r'^[\w.\.]+@\w+\.\D+',post.get('email'))
            if test_str:
                print(test_str[0])

                email_obj = EmailMultiAlternatives(
                    'Varify Your email',
                    f"""Hello dear {request.user},
                    Thanks For visiting our side 💕
                    To Varify your email on <a href="www.google.com"><a>
                    """,
                    settings.EMAIL_HOST_USER,
                    [test_str[0]]
                )
                with open('./templates/chaldal/email.html','r') as f:
                    templates = Template(f.read())
                    vf_obj = Email_Verify.objects.create(profile=request.user.get_profile,email=test_str[0])
                    context = Context({
                        'username':request.user,
                        'varify_link':settings.HOST_NAME +reverse('verify_mail',kwargs={'uuid':vf_obj.key}) if settings.HOST_NAME else f"http://127.0.0.1:8000" +reverse('verify_mail',kwargs={'uuid':vf_obj.key}),
                        'chaldal_img':basic_setting.objects.get().get_logo(),
                        'host':settings.HOST_NAME  if settings.HOST_NAME else "https://chaldal.com/"
                    })
                    full_form_html = templates.render(context)
                email_obj.attach_alternative(full_form_html,'text/html')

                email_obj.send()
            return JsonResponse({"status":"successful"})





from django.db.models import F
def add_customer_bag(request):
    cnt = time()
    POST = request.POST
    if POST:
        if request.user.is_authenticated:
            user_profile = request.user.get_profile
            if POST['type'] == "update":
                try:
                    bag_product = Product.objects.get(pk=POST['prod_id'],city=user_profile.current_city)
                    product_exist = Customer_bags.objects.filter(
                        product=bag_product,
                        profile=user_profile,
                    )
                    if product_exist.exists():
                        print("??????????")
                        product_exist.update(quantity =  POST['quantity'] if int(POST['quantity']) else 1)
                        print(time() - cnt)
                        return JsonResponse({"state":"successful","data":"You have updated the items quantity"})
                    Customer_bags.objects.create(
                        product=bag_product,
                        profile=user_profile,
                        quantity=1
                    )
                    print(time() - cnt)
                    return JsonResponse({"state":"successful",})
                except ValueError:
                    return JsonResponse({"error":"400 Bad request","data":"Don't make bad requests immediately"},status=400)
                except Product.DoesNotExist:
                    return JsonResponse({"state":"faild","data":"This product no longer available"})

            elif POST['type'] == "delete":
                user_profile.get_customerBag_item.filter(product__pk=POST['prod_id']).delete()
                return JsonResponse({"state":"successful",})
            else:
                return JsonResponse({"error":"400 Bad request","data":"Don't make bad requests immediately"},status=400)
        else:return JsonResponse({"error":"Your are not authenticated","data":"Don't make bad requests immediately"},status=400)


def adress_save(request):
    user = request.user.get_profile
    if request.POST:
        get = request.GET
        post = request.POST
        if get.get("map_update"):
           lat= loads(request.POST["map"])["lat"]
           lng = loads(request.POST["map"])["lng"]
           user = request.user.get_profile
           user.location.update_or_create(
                    user = user,
                    defaults={"latitude":lat,"longitude":lng}
                )



           return JsonResponse({"update":"successful"})
        if get.get("get_area"):
            try:
                area = City.objects.get(pk=request.POST.get("city_get")).get_area.all()
                last_added = user.adress.last().area.pk
                html = ''
                for alaka in area:
                    option = "selected" if alaka.pk == last_added else ""
                    html += f"<option {option} value='{alaka.pk}'>{alaka.name}</option>"
                return JsonResponse({"state":"successful","html":html})
            except City.DoesNotExist:
                return JsonResponse({"update":"faild","err":"no area found"})


        if get.get("add_adress"):
            data = loads(post.get("data"))
            city = user.current_city
            area = Area.objects.get(pk=data.get("area"))
            new_adress = user_adress.objects.create(
                user = user ,
                adress = data.get("adress"),
                city = city,
                area = area,
                delivery_parson_name = data.get("name"),
                Phone = data.get("phone"),
            )
            return JsonResponse({"state":"successful","pk":new_adress.pk})

        if get.get("update_adress"):
            print(request.POST)
            data = loads(post.get("data"))
            pk  = data["pk"]
            name  = data["name"]
            adress  = data["adress"]
            phone  = data["phone"]
            city  = user.current_city
            area  = data["area"]
            adress_model = user.adress.filter(pk=pk)
            if adress_model.exists():
                adress_model.update(
                        adress = adress,
                        city = city,
                        area = area,
                        Phone = phone,
                        delivery_parson_name = name,
                        updated_time = now()
                    )
            return JsonResponse({"state":"successful",})
            # return JsonResponse({"state":"faild","err":"404 No Adress found"})

        if get.get("delete"):
            data = loads(post.get("pk"))
            try:
                adress = user.adress.get(pk=data)
                adress.delete()
                return JsonResponse({"state":"successful"})
            except user_adress.DoesNotExist:
                return JsonResponse({"err":"404 error"})

        if get.get("gender"):
            form = gender_from(post)
            if form.is_valid():
                Profile.objects.filter(pk=user.pk).update(gender=form.cleaned_data["gender"])
                return JsonResponse({"state":"successful"})
            return JsonResponse({"err":"404 error"})

        if get.get("profile_name"):
            if post['name']:

                target_user = User.objects.filter(pk=request.user.pk)


                if target_user.exists():
                        try:
                            target_user.update(username=post['name'].strip())
                        except IntegrityError:
                            return JsonResponse({"state":"faild","data":"This name already exists"})

                        return JsonResponse({"state":"successful"})
                return JsonResponse({"err":"404 error"})
            return JsonResponse({"state":"faild","data":"Please fill up your name field 👆. Your name field is empty !!!"})

def get_api(request):
    get = request.GET
    profile = request.user.get_profile

    if get.get("get_city") == "True" and get.get("html") == "True":
        city = City.objects.all()
        cr_city = profile.current_city
        if city.exists():
            all_city = ""
            for i in city:
                option = "selected" if i.Name == cr_city.Name else ""
                all_city += f"<option {option} value='{i.pk}'>{i.Name}</option>"
            return JsonResponse({"state":"successful","html":all_city})
        return JsonResponse({"state":"successful","err":"Opps! not city available in this site"})
    elif get.get("get_city") == "True":
        city = City.objects.all()
        if city.exists():
            all_city = []
            for i in city:
                all_city.append(i.Name)
            return JsonResponse({"state":"successful","data":all_city})
        return JsonResponse({"state":"successful","err":"Opps! not city available in this site"})


from .dynamic import profile_html_render , adressHtml, selectCityHtml
from customer.models import gender_choises
def profile_html(request):
    now = time()

    user_profile = request.user.get_profile
    gender_option_html = ""
    for i in gender_choises:
        check = "selected" if i[0] == user_profile.gender else ""
        gender_option_html+= f"<option  {check} value='{i[0]}'>{i[1]}</option>"
    print(gender_option_html)
    late = time() - now
    print(late)
    return JsonResponse({"status":"successful","html":profile_html_render(user_profile,gender_option_html)})





def map_or_adressHtml(request,type):
    user_profile = request.user.get_profile
    if type == "map":
        with open("/home/shihab2004/Chaldal/dynamicStaric/map.css.txt","r") as f:
            css = f.read()
        with open("/home/shihab2004/Chaldal/dynamicStaric/map.js.txt","r") as f:
            js = f.read()


        html = f"""
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBWOqMTUtC3VgJPQE39tnbIeLM-yAU4Ijw&callback=initMap&libraries=&v=weekly" sync></script>
        {css}
                    [[content]]
                <div id="floating-panel">
                                                [[drop_button]]
                                                <button class="btn btn-light" id="update_location" onclick="getLocation()">Update Your location</button>
                </div>
                                                <div id="map"></div>
        {js}
        """
        lat = user_profile.get_lat_long()["lat"] if user_profile.is_geoLocation() else 23.8103
        lng = user_profile.get_lat_long()["lng"] if user_profile.is_geoLocation() else 90.4125

        html = html.replace("{{get_lat}}",str(lat))
        html = html.replace("{{get_lng}}",str(lng))

        html = html.replace("[[drop_button]]","""<button class="btn btn-light" id="drop" onclick="drop()">Drop Your location</button>""").replace("[[content]]",""" <p style="text-align:center;font-size:15px;font-weight: 600;">Thanks for update your location. We have receive your location.</p>""") if user_profile.is_geoLocation() else html.replace("[[drop_button]]","").replace("[[content]]","""<p style="text-align:center;font-size:15px;font-weight: 600;">Please Update the location to deliver the product to your home</p> """)

    elif type == "localAdress":
        html = adressHtml(user_profile)


    return JsonResponse({"status":"successful","html":html})
    # return HttpResponse(html)








def select_city_Html(request):
    if request.user.is_authenticated:
        user_profile = request.user.get_profile
    else:
        user_profile = None

    html = selectCityHtml(user_profile)
    return HttpResponse(html)







def userBagList(request):
    user_profile = request.user.get_profile
    bagList = []
    for bagItem in user_profile.get_customerBag_item.all():
        bagObj = {
            "amount":bagItem.product.Amount,
            "img":bagItem.product.product_image.first().get_image(),
            "name":bagItem.product.Name,
            "price":bagItem.product.get_discord_price(),
            "product_id":bagItem.product.pk,
            "quantity":bagItem.quantity,
        }
        bagList.append(bagObj)
    # print(bagList)
    return JsonResponse({"status":"successful","data":bagList})




from Product.views import popular
from django.db.models import Max
def checkout(request):
    user_profile = request.user.get_profile
    letest_adress = user_profile.adress.order_by("-updated_time").first()
    if request.GET.get("adress_api") == "true":
        city = user_profile.current_city.Name
        context = []
        for count ,adress in enumerate(user_profile.get_all_adress()):
            adressObj = {
                "pk" :adress.pk ,
                "adress" :adress.adress ,
                "area" : adress.area.name,
                "name" :adress.delivery_parson_name ,
                "phone" :adress.Phone,
                "area_pk":adress.area.pk,
            }
            context.append(adressObj)


        return JsonResponse({"status":"successful","data":context,"crntCity":city})



###################################TIME#####################################################


    today = datetime.datetime.now()
    crnt_ho = int(today.strftime("%H"))
    removed_tt = None
    if  crnt_ho > 20 or crnt_ho < 8: # will change form database
        time = [[((today  + datetime.timedelta(hours=i)).strftime('%I'),(today  + datetime.timedelta(hours=i)).strftime('%p')),((today  + datetime.timedelta(hours=i+1)).strftime('%I'),(today  + datetime.timedelta(hours=i+1)).strftime('%p'))] for i in range(8-crnt_ho,(24 - crnt_ho) -2)]
        isDvToday = True if crnt_ho < 8  else False
    else:
        time = [[((today  + datetime.timedelta(hours=i)).strftime('%I'),(today  + datetime.timedelta(hours=i)).strftime('%p')),((today  + datetime.timedelta(hours=i+1)).strftime('%I'),(today  + datetime.timedelta(hours=i+1)).strftime('%p'))] for i in range(1,(24 - crnt_ho) -2)]
        isDvToday = True
        removed_tt = abs(8 - (20 - (20 - crnt_ho)+1)) # convartion nagative to positive


    mas = [(today  + datetime.timedelta(days=i)).strftime('%B') for i in range(0,7)]
    bar = [(today  + datetime.timedelta(days=i)).strftime('%A') for i in range(2,7)]
    tharik = [(today  + datetime.timedelta(days=i)).strftime('%d') for i in range(0,7)]



###############################Total price calculate form bage################################

    # userAllBags = user_profile.get_customerBag_item.all()
    # print(dir(userBagList(request)))

    bag_json = loads(userBagList(request).content)
    total_price = 0
    price_status = False
    bag_status = False
    if bag_json['status'] == "successful" and bag_json["data"]:
        bag_status = True
        price_status = True
        for bag in bag_json['data']:
            print(bag)
            print("_______________")
            total_price += bag['price'] * bag['quantity']

    elif bag_json['status'] == "successful" and not bag_json["data"]:
        price_status = True
        bag_status = False




    olll_city = City.objects.filter(pk=request.session.get('crnt_city'))
    if olll_city.exists():
        olll_city = olll_city[0].Name
    else:olll_city=""

    if request.session.get('discount_code'):
        obj = user_profile.get_offer_code_obj.filter(code=request.session.get('discount_code'),expiry_date__gte=datetime.datetime.now(),is_used=False)
        if obj:
            total_price = float("{:.2f}".format(total_price - (total_price * (obj[0].discount_parsent/100))))

    delivery_charge = 29

    try:

        dpobj = float(Delivery_Charge_record.objects.filter(if_price__lte=total_price).aggregate(Max("if_price"))["if_price__max"])

        delivery_charge = Delivery_Charge_record.objects.get(if_price=dpobj).delivery_Charge
    except (Delivery_Charge_record.DoesNotExist,TypeError):
        pass

    total_price += delivery_charge



    context ={
        "adress":letest_adress.adress if letest_adress else "",
        "area":letest_adress.area.name if letest_adress else "",
        "city":letest_adress.city.Name if letest_adress else "",
        "panding_delivaryAdress":letest_adress.pk if letest_adress else "",
        "area_option":user_profile.current_city.get_area.all(),
        "defult_number":user_profile.Phone,
        'tarik':tharik,
        "mas":mas,
        "bar":bar,
        "time":time,
        "isDvToday":isDvToday,
        "removed_tt":removed_tt,
        "total_price":total_price,
        "price_status":price_status,
        "bag_status":bag_status,
        "city_from_session":olll_city,
        'root':basic_setting.objects.get(),
        'geolocation':user_profile.get_lat_long() if user_profile.is_geoLocation() else {"lat":23.8103,"lng":90.4125},
        'is_use_geo_google': user_profile.is_geoLocation(),
        'reusable_bag_price':basic_setting.objects.get().reusable_bag_price,
        "delivery_charge":delivery_charge
    }

#########!!==>  url routhin hare👇  <==!!##################
    if request.GET.get("matRout"):
        # context.update({"mar_routing":reverse("customer:checkout")})
        return render(request,'chaldal/customer/checkout.html',context)


    routing_url = reverse("customer:checkout")+"?matRout=True"
    return popular(request,routhing={"mat_router":routing_url})



from .utils import get_adress
def paymentView(request):

    bag_json = loads(userBagList(request).content)
    user_profile = request.user.get_profile
    if request.POST:
        print(request.POST)
        try:
            json_request = loads(request.POST['data'])
            delivery_time = json_request['dVtime']
            delivery_date = json_request['dVdate']
            user_adress_id = json_request['selectedCityId']
            reusableBag_status = json_request['reusableBag']

            reusableBag_price = 0
            adress_obj = None

            print(json_request)
            if json_request['reusableBag'] == "on":
                reusableBag_price = basic_setting.objects.get().reusable_bag_price
            #facing userADress
            user_home_adress = get_adress(user_profile,user_adress_id)
            if not user_home_adress:
                return HttpResponseBadRequest("BAD REQUEST NO ADDRESS FOUND")

            #***************** serialize date and time *****************

            day = delivery_date.split("-")[0]
            mounth = delivery_date.split("-")[1]
            year = datetime.datetime.now().strftime('%Y')

            hour = delivery_time.split("_")[1].split(":")[0]
            hour_am_Pm = delivery_time.split("_")[1].split("-")[1]

            date_obj = datetime.datetime.strptime(f"{day}/{mounth}/{year} {hour}:{hour_am_Pm}",'%d/%B/%Y %I:%p')
            valid_llc = True
            for productItem in bag_json['data']:
                d_obj = Product.objects.get(pk=productItem['product_id'])
                __prsent_product_number = int(d_obj.Stoke_quantity)
                if (not __prsent_product_number) or 0 >= (d_obj.Stoke_quantity - int(productItem.get('quantity'))):
                    valid_llc = False
                    __product__name = d_obj.Name
                    break

            if valid_llc:
                discount_code_found = user_profile.get_offer_code_obj.filter(code=request.session.get('discount_code'),expiry_date__gte=datetime.datetime.now(),is_used=False)
                if discount_code_found:

                    bag_json['discount_parsent'] = discount_code_found[0].discount_parsent
                    discount_code_found[0].is_used = True
                    discount_code_found[0].save()
                    del request.session['discount_code']
                # ----------------------> Google map code <-----------------------
                geo_location__obj__ = None
                if json_request['address_type'] == 'map':
                    geo_location__obj__ = user_profile.location.first()


                order_obj = Order(
                    profile=user_profile,
                    track_ip=request.META['REMOTE_ADDR'],
                    home_adress=user_home_adress,
                    delivery_time= date_obj,
                    bag_json= dumps(bag_json),
                    reusableBag_price=reusableBag_price,
                    geo_location=geo_location__obj__,
                    discount_offer=bag_json.get('discount_parsent')
                )


                if order_obj:
                    order_obj.save()



                    for productItem in bag_json.get('data'):
                        pd_obj = Product.objects.get(pk=productItem['product_id'])
                        if pd_obj.Stoke_quantity:

                            pd_obj.Stoke_quantity = pd_obj.Stoke_quantity - productItem['quantity']
                            pd_obj.save()

                            order_obj.product.add(productItem['product_id'])




                    #-----------------> EMAIL PART <-----------------------
                    if user_profile.user.email:
                        email_obj = EmailMultiAlternatives(
                            'Varify Your email',
                                f"""Hello dear {request.user},
                                Thanks For visiting our side 💕
                                To Varify your email on <a href="www.google.com"><a>
                                """,
                                settings.EMAIL_HOST_USER,
                                [user_profile.user.email]
                        )
                        __is__discount = bag_json.get('discount_parsent')

                        __totalPrice__ = 0
                        for item in  bag_json.get('data'):
                            __totalPrice__ += float(item['price']) * int(item['quantity'])



                        if __is__discount:
                            __subTotalPrice__ = __totalPrice__
                            __discountPrice__ = (__totalPrice__ * (__is__discount/100))
                            __totalPrice__ = (__totalPrice__ - float(__discountPrice__)) + float(reusableBag_price)
                        else:
                            __subTotalPrice__= __totalPrice__
                            __discountPrice__ = 0
                            __totalPrice__ = __totalPrice__



                        dly_charge = order_obj.order_delivery_charge()



                        with open('/home/shihab2004/Chaldal/templates/chaldal/extra/product_mail.html','r') as f:
                            templates = Template(f.read())
                            context = Context({
                            'order':bag_json.get('data'),
                            'profile':user_profile,
                            'reusableBag_price':reusableBag_price,
                            "subTotal":"{:.2f}".format(__subTotalPrice__),
                            "discount":"{:.2f}".format(__discountPrice__),
                            'totalPrice':float("{:.2f}".format(__totalPrice__)) + float(dly_charge),
                            'host':settings.HOST_NAME,
                            "delivery_charge":dly_charge
                            })
                            full_form_html = templates.render(context)
                        email_obj.attach_alternative(full_form_html,'text/html')
                        email_obj.send()




                    user_profile.get_customerBag_item.all().delete()


                routing_url = reverse("customer:payment")+f"?matRout=True&orderId={order_obj.pk}"
                return JsonResponse({"status":"successful","matRout":routing_url,"isLocalSessionclear":True})




            return JsonResponse({"err":"Order error",'data':f'The <em>{__product__name}</em> product is out of stoke'})
        except (KeyError,IndexError,): #ValueError
            return HttpResponse("404 Client Error",status=404)
    else:

        if request.GET.get("matRout") and request.GET.get("orderId"):



            #======> fatching order from user profile
            try:
                user_order = user_profile.get_user_order.get(pk=request.GET.get("orderId"))
            except (Order.DoesNotExist,ValueError):
                return HttpResponseBadRequest("Bad request No Order found!")


            Delivery_Time_obj = user_order.delivery_time

            to_time_dly = Delivery_Time_obj - datetime.timedelta(hours=1)


            #=======> fatching time obj 👆
            if not user_order.order_status == "CN":

                bag_json = loads(user_order.bag_json)

                __geo__ = {"status":False}
                if user_order.is_use_geo_location():
                    __geo__.update({
                        "status":True,
                        **user_order.get_lat_lng()
                    })



                reusableBag_price = user_order.reusableBag_price

                context= {
                    "total_price":user_order.product_total(),
                    "delivery_charge":user_order.order_delivery_charge(),
                    "reusablePrice":reusableBag_price,
                    "discount_offer":user_order.total_price(discont_price=True),
                    "order_total":user_order.total_price(),
                    "orderId":user_order.pk,
                    "Delivery_Address":user_order.home_adress.adress,
                    "Delivery_day":Delivery_Time_obj.day,
                    "Delivery_mounth":Delivery_Time_obj.strftime("%h"),
                    "Delivery_from_time":f"{Delivery_Time_obj.strftime('%I')}:00 {Delivery_Time_obj.strftime('%p')}",
                    "Delivery_to_time":f"{to_time_dly.strftime('%I')}:00 {to_time_dly.strftime('%p')}",
                    "MEDIA_URL":settings.MEDIA_URL,
                    'Instructions':user_order.Instructions,
                    "geo":__geo__,
                }
                print(context)
                return render(request,'chaldal/customer/payment.html',context)

            elif user_order.order_status == "CN":
                context= {
                    "orderId":user_order.pk,
                    "Delivery_Address":user_order.home_adress.adress,
                    "Delivery_day":Delivery_Time_obj.day,
                    "Delivery_mounth":Delivery_Time_obj.strftime("%h"),
                    "Delivery_from_time":f"{Delivery_Time_obj.strftime('%I')}:00 {Delivery_Time_obj.strftime('%p')}",
                    "Delivery_to_time":f"{to_time_dly.strftime('%I')}:00 {to_time_dly.strftime('%p')}",
                    "MEDIA_URL":settings.MEDIA_URL
                }

                return render(request,'chaldal/customer/cancelOrder.html',context)



        routing_url = reverse("customer:payment")+r"?matRout=True&orderId=%s" % request.GET.get("orderId")
        return popular(request,routhing={"mat_router":routing_url})



def userOrderDetail(request):
    user_profile = request.user.get_profile

    if request.POST:
        if request.GET.get('orderReport'):
            report_decode = loads(request.POST['data'])
            forms = order_report_form(report_decode)
            if forms.is_valid():
                order_obj = user_profile.get_user_order.filter(pk=forms.cleaned_data['orderId'])
                if order_obj.exists:
                    if order_obj[0].order_status == 'SF':

                        order_obj.update(
                            order_report=forms.cleaned_data['report']
                        )

                        return JsonResponse({"status":"successful"})
                return JsonResponse({"status":"faild","data":"404 No order found!"},status=404)

            return JsonResponse({"status":"error","data":"Bad request don't try againg"},status=400)

        elif request.GET.get('uploadStar'):
            forms = order_star_submit(request.POST)
            if forms.is_valid():
                order_obj = user_profile.get_user_order.filter(pk=forms.cleaned_data['orderId'])
                if order_obj.exists:
                    if order_obj[0].order_status == 'SF':
                         order_obj.update(
                            stars=forms.cleaned_data['rating']
                        )
                return JsonResponse({"status":"successful"})
            return JsonResponse({"status":"error","data":"Bad request don't try againg"},status=400)


    elif request.GET.get('api'):

        full_order_data = []
        for order in user_profile.get_user_order.all().order_by('-pk'):

            Delivery_Time_obj = order.delivery_time
            to_time_dly = Delivery_Time_obj - datetime.timedelta(hours=1)

            order_data ={
                "total_price":order.total_price() if not order.order_status == "CN" else 0,
                "orderId":order.pk,
                "order_stars":order.stars,
                "order_status":order.get_order_status_display(),
                "productId":[iD.pk for iD in order.product.all()],
                "home_adress":order.home_adress.adress,
                "bag_json":loads(order.bag_json),
                "Delivery_from_time":f"{Delivery_Time_obj.strftime('%I')}:00 {Delivery_Time_obj.strftime('%p')}",
                "Delivery_to_time":f"{to_time_dly.strftime('%I')}:00 {to_time_dly.strftime('%p')}",
                "Delivery_Date":to_time_dly.strftime('%D'),
                "ISorder_reported": True if order.order_report else False
            }

            full_order_data.append(order_data)

        return JsonResponse({"status":"successful","data":full_order_data,"order_report":report_choise})

    elif request.GET.get("matRout"):
        context = {
            "isNeedObj": True if request.GET.get("obj") else False
        }
        return render(request,'chaldal/customer/order_detail.html',context)

    routing_url = reverse("customer:userOrdered")+"?matRout=True&obj=True"
    return popular(request,routhing={"mat_router":routing_url})




def payment_history(request):
    if request.POST:
        user_profile = request.user.get_profile
        try:
            form_time = datetime.datetime.strptime(f'{request.POST.get("year")} {request.POST.get("mounth")}',"%Y %b")
            to_time = (form_time.replace(month=int(form_time.strftime('%m'))+1,hour=23,minute=59,second=59,microsecond=999999) if not form_time.month == 12 else form_time.replace(year=int(form_time.strftime('%Y'))+1,hour=23,minute=59,second=59,microsecond=999999,month=1)) - datetime.timedelta(days=1)
            all_orders = user_profile.get_user_order.filter(ordered_time__gte=form_time,ordered_time__lte=to_time,order_status='SF')
            if all_orders.exists():
                order_list = []
                for orders in all_orders:
                    order_list.append({
                        'Date':orders.ordered_time.strftime('%b %d'),
                        'Description':orders.get_description(),
                        'payment_method':orders.payment_method.Name,
                        'price':orders.total_price()
                    })

                return JsonResponse({"status":"successful",'data':order_list})
            return JsonResponse({"status":"faild",'data':'no data found'})
        except ValueError:
            return JsonResponse({"status":"Bad request",'data':"Don't inject any bad request"},status=400)

    elif request.GET.get('matRout'):
        today = datetime.datetime.today()
        all_time = [today]
        for i in range(12):
            pasent_time = all_time[i].replace(day=1)
            previous_mounth = pasent_time - datetime.timedelta(days=1)
            if not previous_mounth.strftime("%Y") == all_time[0].strftime("%Y"):
                break
            all_time.append(previous_mounth)

        all_mounth_gone = []
        for i in all_time:
            all_mounth_gone.append(i.strftime('%b'))

        next_mounths = []
        for i in range(int(today.strftime("%m"))+1,13):
            next_mounth = datetime.datetime.today().replace(month=i,day=1)
            next_mounths.append(next_mounth.strftime('%b'))
        context = {
            "previous_ago":all_mounth_gone[::-1],
            "next_year":next_mounths
        }
        return render(request,'chaldal/customer/payment_history.html',context)

    routing_url = reverse("customer:payment_history")+"?matRout=True"
    return popular(request,routhing={"mat_router":routing_url})



def render_city(request):
    if request.GET.get('matRout'):
       return select_city_Html(request)

    routing_url = reverse("customer:select_city")+"?matRout=True"
    return popular(request,routhing={"mat_router":routing_url})





def post_data3(request):
    if request.POST:

        if request.GET.get('add_previous_item_to_card'):
            try:

                order = request.user.get_profile.get_user_order.get(pk=request.POST.get('order_id'))
                product_json = loads(order.bag_json)

            except Order.DoesNotExist:
                return JsonResponse({"status":"error","data":"No order Found"},status=404)
            except ValueError:
                return JsonResponse({"status":"error","data":"Bad Request"},status=400)

            context ={'sucsses_product':[],'faild_product':[]}
            if product_json.get('status') == "successful":
                    for item in product_json.get('data'):

                        # Customer_bags.create(
                        #
                        # )

                        product = Product.objects.get(pk=item.get('product_id'))
                        qnt = 0

                        if product.Stoke_quantity >= item.get('quantity') and product.Stoke_quantity:
                            if product.Stoke_quantity >= item.get('quantity'):

                                qnt = item.get('quantity')
                            else:
                                not_abailable = abs(product.Stoke_quantity - item.get('quantity'))
                                qnt = item.get('quantity') - not_abailable

                            if qnt:
                                context['sucsses_product'].append({
                                'name':product.Name,
                                'qnt':qnt,
                                "Price":product.Price,
                                "discord_price":product.get_discord_price(),
                                'img':product.product_image.first().get_image(),
                                'amount':product.Amount,
                                'product_id':product.pk
                                })

                                omj = Customer_bags.objects.filter(
                                    profile=request.user.get_profile,
                                    product=product
                                )

                                if omj.exists():
                                    omj.update(quantity=qnt)
                                else:

                                    Customer_bags.objects.update_or_create(
                                        profile=request.user.get_profile,
                                        product=product,
                                        quantity=qnt
                                    )

                        else:
                            not_abailable = abs(product.Stoke_quantity - item.get('quantity'))

                            context['faild_product'].append({
                                'name':product.Name,
                                'qnt':not_abailable,
                                "Price":product.Price,
                                "discord_price":product.get_discord_price(),
                                'img':product.product_image.first().get_image(),
                                'amount':product.Amount,
                                'product_id':product.pk
                            })

                            if product.Stoke_quantity >= item.get('quantity'):

                                qnt = item.get('quantity')
                            else:
                                not_abailable = abs(product.Stoke_quantity - item.get('quantity'))
                                qnt = item.get('quantity') - not_abailable

                            if qnt:
                                context['sucsses_product'].append({
                                'name':product.Name,
                                'qnt':qnt,
                                "Price":product.Price,
                                "discord_price":product.get_discord_price(),
                                'img':product.product_image.first().get_image(),
                                'amount':product.Amount,
                                'product_id':product.pk
                                })

                                omj = Customer_bags.objects.filter(
                                    profile=request.user.get_profile,
                                    product=product
                                )
                                if omj.exists():
                                    omj.update(quantity=qnt)
                                else:

                                    Customer_bags.objects.update_or_create(
                                        profile=request.user.get_profile,
                                        product=product,
                                        quantity=qnt
                                    )





            return JsonResponse({"status":"successful",'data':context})

        elif request.GET.get('reportOrder'):
            if request.user.is_authenticated:
                try:

                    order = request.user.get_profile.get_user_order.get(pk=request.POST.get('orderId'))
                    # order.update(order_status="Cancelled")
                    if request.POST.get('report') and request.POST.get('report') != "None":
                        form = order_report_form(request.POST)
                        if form.is_valid():
                            order.order_status = "CN"
                            order.order_report = form.cleaned_data['report']
                    else:
                        order.order_status = "CN"
                    print(order)
                    order.save()
                except:
                    return JsonResponse({"status":"faild","data":"bad request"},status=400)

                return JsonResponse({"status":"successful"})

        order = request.user.get_profile.get_user_order.get(pk=request.POST.get('orderId'))
        order.Instructions = request.POST.get('instructions')
        order.save()
        return JsonResponse({"status":"successful"})
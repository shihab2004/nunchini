from json import loads
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from ADMIN.models import chat_list
from corporate.models import root
from customer.models import Profile,C8Message,ActiveUser,Email_Verify
from django.contrib.auth.models import User
from root.models import basic_setting
# Create your views here.

def llc(request):
    user_profile = request.user.get_profile
    context = {
        "chat_room":user_profile.pk
    }
    return render(request,'chaldal/extra/live_chat.html',context)

from root.utils import super_user_required

@super_user_required
def admin_chat(request):

 
        if request.GET.get('get_member_c8'):
            all_messages = []
            try:
                c8Obj = C8Message.objects.filter(roomId=request.GET.get('get_member_c8'))
                if c8Obj.exists():
                    for message in c8Obj:
                        all_messages.append({
                        'pk':message.pk,
                        'profile_pk':message.profile.pk,
                        'message':message.message
                    })
                    return JsonResponse({"status":"successful",'data':all_messages})
                return JsonResponse({"status":"faild",'data':"no message found"})
            except ValueError:
                return JsonResponse({"status":"Bad request"},status=400)


        elif request.GET.get('get_active_all_member'):
            all_active_profile = []
            
            for profile in ActiveUser.objects.filter(is_active=True):
                all_active_profile.append({
                    "client_id":profile.profile.pk,
                    'username':profile.profile.user.username,
                    'profile_photo':profile.profile.profile_photo.url
                })
            return JsonResponse({"status":"successful",'data':all_active_profile})



        user_profile = request.user.get_profile
        
        c8_list = []
        for clist in loads(chat_list.objects.get(admin_profile=user_profile).lists).get("clist"):
          
            pp = Profile.objects.get(pk=clist)
            c8_list.append({
                "profile":pp,
                "message": C8Message.objects.filter(profile=pp).order_by("-created_time").first(),
                "active_status":"asd"
            })
           
        context = {
            "chat_room":user_profile.pk,
            'user_name':request.user.username,
            'img':user_profile.profile_photo.url,
            "c8_list":c8_list
        }
        
        return render(request,'admin/admin_live_c8.html',context)


from django.urls import reverse
from django.contrib.auth.forms import  AuthenticationForm , PasswordChangeForm
from Product.views import popular
from django.contrib.auth import authenticate , login , logout
from root.forms import CreateUserForm , AuthForm
from django.shortcuts import redirect
from re import findall
def signup(request):
    if request.GET.get('matRout'):
        if request.POST:
            print(request.POST)
            if not request.POST.get('current_city'):
                return JsonResponse({"status":"err","data":"Fill up your Current City👇"})
            if not request.POST.get('Phone'):
                return JsonResponse({"status":"err","data":"Phone number is required. Please fill this"})
            Phone = request.POST.get('Phone')
            if len(Phone) == 11 or (Phone.startswith("+88") and len(Phone) == 14):
                is_phone = findall(r'^(\+880|0)1(9|7|8|5|3|6)\d+$',Phone)
                if not is_phone:
                    return JsonResponse({"status":"err","data":"Your Phone Number is Invalid. Phone Number must be a bangladeshi number😅"})
            else:
                    return JsonResponse({"status":"err","data":"Your Phone Number is Invalid. Please corrent and ensure your Phone Number😐"})

            form = CreateUserForm(request.POST,request.FILES)
            print(form.is_valid())
            if form.is_valid():
                ip_addr = request.META['REMOTE_ADDR']
                user_new_model = form.save()
                
                gender = form.cleaned_data['gender']
                Phone = form.cleaned_data['Phone']
                current_city = form.cleaned_data['current_city']
                user_new_profile = Profile.objects.create(
                    user = user_new_model,
                    profile_photo=form.cleaned_data['profile_photo'],
                    ip_addr = ip_addr,
                    gender=gender,
                    Phone = Phone,
                    current_city = current_city
                )
                ActiveUser.objects.create(
                    profile=user_new_profile
                )
                # print(Phone)
                print(user_new_profile)
                print(Phone)
                print(current_city)

                print(ip_addr)
                print(form.cleaned_data['profile_photo'])
             
                print("___________________________")
                return JsonResponse({"status":"succsess","url":"/login"})
            
            username=request.POST.get('username')
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            
            if password1 != password2:
                return JsonResponse({"status":"err","data":"Your password doesn't match😅. Please Valid your password"})


            
            u = User.objects.filter(username=username)
            if u.exists():
                return JsonResponse({"status":"err","data":"Please change your username🙂. The username already exists😶"})
                
       
            return JsonResponse({"status":"err","data":"Please valid your form!😅 Please Change Your Password and Ensure the  Form"})

        form = CreateUserForm()
        url = reverse("signup")
        return render(request,'chaldal/customer/login.html',{'form':form,'url':url,'is_signUpForm':True})
    routing_url = reverse("signup")+"?matRout=True"
    return popular(request,routhing={"mat_router":routing_url})



def loginView(request):
    if request.GET.get('matRout'):
        if request.POST:
            
            authForms = AuthForm(request.POST)
            if authForms.is_valid():
            
            

                user_model = authenticate(username=authForms.cleaned_data['username'],password=authForms.cleaned_data['password'])
                if user_model:
                    print('///////////////////////////////////')
                    print('///////////////////////////////////')
                    print('///////////////////////////////////')
                    print(user_model)
                    wait_for_it = login(request,user_model)
                    print(wait_for_it)
            

                    return JsonResponse({"status":'succsess','url':'/'})
                    

        form = AuthenticationForm()
        url = reverse("login")
        return render(request,'chaldal/customer/login.html',{'form':form,'url':url})
    routing_url = reverse("login")+"?matRout=True"
    return popular(request,routhing={"mat_router":routing_url})



def logOutview(request):
    if request.user.is_authenticated:
   
        logout(request)
 
    return redirect('/')


def verify_email(request,uuid):
    try:
        obj = Email_Verify.objects.get(key=uuid)
        obj.profile.user.email = obj.email
        obj.profile.user.save()
        obj.delete()
        return redirect('/customer/profile/')
    except Email_Verify.DoesNotExist:
        pass
    return HttpResponse("404 Error",status=404)



def change_password(request):
    if request.GET.get('matRout'):
        if request.POST:
            forms = PasswordChangeForm(user=request.user,data=request.POST)

            print(forms.is_valid())
            print(forms.errors)
            if forms.is_valid():
                forms.save()
                return JsonResponse({"status":'succsess','data':'Your Password Succsessfully Changed 🤗'})

            return JsonResponse({"status":'err','data':forms.errors})
           
        return render(request,'chaldal/customer/change_password.html')
    routing_url = reverse("customer:change_password")+"?matRout=True"
    return popular(request,routhing={"mat_router":routing_url})



import datetime
def next_dlv_time(request):
   
    today = datetime.datetime.now()
    crnt_ho = int(today.strftime("%H"))
    if  crnt_ho > 20 or crnt_ho < 8: # will change form database
        time = [[((today  + datetime.timedelta(hours=i)).strftime('%I'),(today  + datetime.timedelta(hours=i)).strftime('%p')),((today  + datetime.timedelta(hours=i+1)).strftime('%I'),(today  + datetime.timedelta(hours=i+1)).strftime('%p'))] for i in range(8-crnt_ho,(24 - crnt_ho) -2)]
        isDvToday = True if crnt_ho < 8  else False
    else:
        time = [[((today  + datetime.timedelta(hours=i)).strftime('%I'),(today  + datetime.timedelta(hours=i)).strftime('%p')),((today  + datetime.timedelta(hours=i+1)).strftime('%I'),(today  + datetime.timedelta(hours=i+1)).strftime('%p'))] for i in range(1,(24 - crnt_ho) -2)] 
        isDvToday = True
    

    return JsonResponse({"status":'succsess',"isDvToday":isDvToday,"data":time[0]})

def error_404(request):
    
    return render(request,"chaldal/404.html",{"fav":basic_setting.objects.get().get_favicon(),"copyring":datetime.date.today().year})
    
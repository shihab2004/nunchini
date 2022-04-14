from json import loads
from django.http import JsonResponse
from django.shortcuts import render
from Product.views import popular
from django.urls import reverse
from .models import support_menu , Team
from django.template import Template , Context
from root.models import basic_setting
# Create your views here.
from django.views.decorators.cache import cache_page
from django.conf import settings


def mainView(request,slug):


    if request.GET.get('matRout'):
        if request.GET.get('popstate'):
            popstate = True
        else:
            popstate=False

        all_menu = support_menu.objects.all()
        return render(request,'chaldal/support/qs_as.html',{'menus':all_menu,'crnt_menu':slug,"popstate":popstate,"MEDIA_URL":settings.MEDIA_URL})

    routing_url = reverse("support:mainView",kwargs={"slug":slug})+"?matRout=True"
    return popular(request,routhing={"mat_router":routing_url})







def api(request):
    if request.GET.get('menu'):
        try:
            menu = support_menu.objects.get(slug=request.GET.get('menu'))
        except support_menu.DoesNotExist:
            return JsonResponse({"status":"faild",'data':'404 error'},status=404)

        context={
            'status':'successful',
            'menu_name':menu.name,
            'data':menu.body,
            'img':menu.img.url,
            'section':None
        }
        if request.GET.get('menu') == 'team':
            with open('/home/shihab2004/Chaldal/templates/chaldal/support/team_members.html','r') as f:
                team_html = f.read()
                all_team_members = []
                for members in Team.objects.all():
                    all_team_members.append({
                        'photo':members.photo.url,
                        'name':members.name,
                        'occupation':members.occupation,
                        'discription':members.discription,
                    })
                context.update({
                    'team_html':team_html,
                    'team_members_data':all_team_members,
                    'section':'team'
                })
        elif request.GET.get('menu') == 'contact-us':

            with open('/home/shihab2004/Chaldal/templates/chaldal/support/contuct-us-form.html','r') as f:
                templates = Template(f.read())
                context2 = Context({
                    "is_auth":request.user.is_authenticated,
                    'name':request.user if request.user.is_authenticated else "",
                    'email':request.user.email if request.user.is_authenticated else "",
                    'phone2':request.user.get_profile.Phone if request.user.is_authenticated else "",
                    "phone":basic_setting.objects.get().Mobile.all()[0].Phone
                })
                full_form_html = templates.render(context2)
                context.update({
                    'section':'contact-us',
                    'form_html':full_form_html
                })

        return JsonResponse(context)


from .forms import ContactUsForm
from re import match
def helpPost(request):
    user_profile = request.user.get_profile if request.user.is_authenticated else None
    data = loads(request.POST['data'])
    is_match = match('^(\+880|0)1(9|8|7|6|5|3)\d+',data['number'])
    if is_match:
        if len(is_match.string) < 14 or len(is_match.string) < 13 or len(is_match.string) < 10 or len(is_match.string) < 11:
            print('########################################')

            cous_form = ContactUsForm({
            'profile':user_profile,
            "name":data['name'],
            "email":data['email'],
            "number":is_match.string,
            "message":data['message'],
            "status":"N"
            })
            print(cous_form.errors)
            if cous_form.is_valid():
                cous_form.save()
                return JsonResponse({"status":"successful",'data':"Thanks for dropping us a note. We'll get back to you within 24 hours. For urgent matters, please call our hotline: 0188-1234567"})
        return JsonResponse({"status":"faild",'data':"Invalid Forms"})

    return JsonResponse({"status":"error",'data':"Invalid Number"})


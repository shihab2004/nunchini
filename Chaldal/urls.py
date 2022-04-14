"""Chaldal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http.response import HttpResponse , JsonResponse
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from index.views import index
from django.views.decorators.csrf import csrf_exempt

from root.views import *


def a(request):
    if request.POST:
        print(request.POST)


    return HttpResponse()
from django.middleware.csrf import get_token

@csrf_exempt
def OMG(request):
    if request.POST:
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


    # request.session['Matols'] = "sdad"
    # print(request.POST)
    print(request.session.session_key)
    print(request.POST)
    print(request.FILES)
    # print(get_token(request))
    alu = {request.POST.get("UserName"):request.POST.get("Password")}
    print(request.POST.get("Image"))
    print(alu)
    return JsonResponse(alu)

urlpatterns = [
    path("turoLove/",OMG),
    path('home/', index,name="index"),
    path('favicon.ico/', a),
    path("admin/",include("ADMIN.urls",namespace="ADMIN")),
    path('admin/chat/', admin_chat),
    path('admina/', admin.site.urls),
    path('signup/',signup,name="signup"),
    path('login/',loginView,name="login"),
    path('logout/',logOutview,name="logout"),
    path("t/",include("support.urls",namespace="support")),
    path('corporate/',include('corporate.urls',namespace='corporate')),
    path("",include("Product.urls",namespace="product")),
    path("customer/",include("customer.urls",namespace="customer")),
    path('verify/<uuid>/',verify_email,name="verify_mail"),
    path('get/next_dlv_time/',next_dlv_time,name="next_dlv_time")

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

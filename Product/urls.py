from django.http.response import HttpResponse
from django.urls import path
from .views import api_api, popular,Product_view,product_detailView,menuImageApi,p8ModalHtml,product_search,Product_Offer,product_request

app_name = "product"
def ss(requ):
    print(requ.user)
    print(requ.user.get_profile.current_city)
    return HttpResponse()

urlpatterns = [
    path("llll/",ss,name="index"),
    path("",popular,name="index"),
    path("<slug>/",Product_view,name="Menu"),
    path("product/offer/",Product_Offer,name="offer"),
    path("product/<slug>/",product_detailView,name="product_detail_view"),
    path('search/<slug>/',product_search,name='productSearch'),

    # api
    path("api/menu_img/<slug>/",menuImageApi,name="menu-image-api"),
    path("api/p8Modal/",p8ModalHtml,name="p8ModalHtml"),
    path("api/product/request/",product_request,name="product_request"),
    path('api/api/',api_api,name='api')
]

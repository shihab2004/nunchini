from django.urls import path
# from .views import profile,adress_save,get_api,profile_html,map_or_adressHtml,select_city_Html,post_data2,add_customer_bag,userBagList,checkout,paymentView
from .views import *
from root.views import change_password

app_name="customer"

urlpatterns = [
    path("profile/",profile),
    path("orders/",userOrderDetail,name="userOrdered"),
    path("account-history/",payment_history,name="payment_history"),
    path("select-city/",render_city,name="select_city"),
    path("changepassword/",change_password,name="change_password"),
    
    # order information
    path("checkout/",checkout,name="checkout"),
    path("checkout/payment/",paymentView,name="payment"),
    # api
    path("api/post/",adress_save,name="post_data"),
    path("api/post/add_bag/",add_customer_bag,name="add_bag"),
    path("api/post2/",post_data2,name="post_data2"),
    path("api/post3/",post_data3,name="post_data3"),
    path("api/get/",get_api,name="get_api"),
    path("api/get/html/",profile_html,name="get-profile-html"),
    path("api/get/adress_html/<str:type>/",map_or_adressHtml),
    path("api/get/select-city/",select_city_Html,name="select_city_html"),
    # api get data form bag database
    path("api/get/itemBagList/",userBagList,name="bagList"),

]

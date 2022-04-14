from django.urls import path
from .views import *
app_name = "ADMIN"


urlpatterns = [
    path("login/",login_admin,name="login_admin"),
    path("",Home,name="admin_home"),
    
    
    
    path("profile/<int:pk>/",user_profile,name="user_profile"),
    
    
    #root
    path("root/",admin_root,name="admin_root"),
    path("root/mobile/delete/<int:pk>/",delete_mobile,name="admin_root"),
    #Menu
    path("menu/product_menu/",product_menu,name="product_menu"),
    path("menu/product_menu/create/",product_menu_create,name="product_menu_create"),
    path("menu/product_menu/details/<int:pk>/",product_menu_details,name="product_menu_details"),
    path("menu/product_menu/delete/<int:pk>/",product_menu_delete,name="product_menu_delete"),
    
    path("menu/home/",home_menu,name="home_menu"),
    path("menu/home/create/",home_menu_create,name="home_menu_create"),
    path("menu/home/details/<int:pk>/",home_menu_details,name="home_menu_details"),
    path("menu/home/delete/<int:pk>/",home_menu_delete,name="home_menu_delete"),
    
    
    
    path("menu/help_more/",help_more_menu,name="help_more_menu"),
    path("menu/help_more/create/",help_more_create,name="help_more_create"),
    path("menu/help_more/details/<int:pk>/",help_more_details,name="help_more_details"),
    path("menu/help_more/delete/<int:pk>/",help_more_delete,name="help_more_delete"),
    
    
    
    
    
    path("menu/footer/",footer_menu,name="footer_menu"),
    path("menu/footer/create/",footer_menu_create,name="footer_menu_create"),
    path("menu/footer/details/<int:pk>/",footer_menu_details,name="footer_menu_details"),
    path("menu/footer/delete/<int:pk>/",footer_menu_delete,name="footer_menu_delete"),
    
    
    path("menu/footer_sub/",footer_menuSub,name="footer_menuSub"),
    path("menu/footer_sub/create/",footer_menuSub_create,name="footer_menuSub_create"),
    path("menu/footer_sub/details/<int:pk>/",footer_menuSub_details,name="footer_menuSub_details"),
    path("menu/footer_sub/delete/<int:pk>/",footer_menuSub_delete,name="footer_menuSub_delete"),
    
    
    
    
    path("delivery_man/",delivery_man12,name="delivery_man"),
    path("delivery_man/create/",delivery_man12_create,name="delivery_man_create"),
    path("delivery_man/details/<int:pk>/",delivery_man12_update,name="delivery_man_update"),
    path("delivery_man/delete/<int:pk>/",delivery_man12_delete,name="delivery_man_delete"),
    
    
    path("mail/",mail,name="mail"),
    path("mail/details/<int:pk>/",mail_details,name="mail_details"),
    
    
    path("order/",admin_order_list,name="admin_order_list"),
    path("order/details/<int:pk>/",admin_order_details,name="admin_order_details"),
    path("order/details/<int:pk>/",admin_order_details,name="admin_order_details"),
    path("order/details/<int:pk>/pdf/",admin_order_pdf,name="admin_order_pdf"),
    
    
    
    path("product/",admin_product_list,name="admin_product_list"),
    path("product/details/<int:pk>/",admin_product_list_details,name="admin_product_list_details"),
    path("product/create/",admin_product_create,name="admin_product_create"),
    path("product/delete/<int:pk>/",admin_product_delete,name="admin_product_delete"),
    
    #Business Code
    path("business/client/",business_client,name="business_client"),
    path("business/corporate/",business_corporate,name="business_corporate"),
    path("business/request/",business_request,name="business_request"),
    path("business/request/view/<int:pk>/",business_request_view,name="business_request_view"),
    
    
    path("d_feature/",d_feature,name="d_feature"),
    path("notification/",notification_view,name="notification_view"),
    path("p_request/",p_request,name="product_request"),
    
    
    path("city/",city_view,name="city_view"),
    
    path("area/",area_view,name="area_view"),
    
    
    path("team/",team,name="team"),
    
    
    
    path("offer_code/",offer_code,name="offer_code"),
]

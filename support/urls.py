from django.urls import path ,re_path
from support.views import *

app_name = 'support'

urlpatterns = [
    path('api/',api,name='api'),
    path('post/',helpPost,name='contuctUs'),
    path('<slug>/',mainView,name='mainView'),

    # path('AboutUs/')
]

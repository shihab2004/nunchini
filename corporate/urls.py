from django.urls import path
from .views import *

app_name="corporate"

urlpatterns = [
    path("",corporateIndex,name="index"),

]

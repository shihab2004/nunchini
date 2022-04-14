import imp
from root.models import Menu
from django import template
from root.models import basic_setting
register = template.Library()

@register.filter
def get_item(dictionary, key):
      return dictionary[key]


@register.filter
def get_name(pk):
      try:
            return Menu.objects.get(pk=pk).Name
      except:
            return None
      
      
from re import split
@register.filter
def get_svg_text_form_file(file):
    
    if file:
        text = split(r"<svg",file.read().decode())
        return "<svg"+text[1]
    return ""


@register.filter
def total_per_price(qnt,price):
      return int(qnt) * int(price)




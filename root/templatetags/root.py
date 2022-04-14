from django import template
from root.models import basic_setting
register = template.Library()

@register.filter
def get_favicon(asd):
    
      return basic_setting.objects.get().get_favicon()

@register.filter
def get_total(price,qnt):
 
      return int(price) * int(qnt)


from django import template

register = template.Library()

@register.filter
def option_filter(name,c_name):
   if c_name == name:
          return "selected"
   return ""

@register.filter
def user_city_option_filter(city,c_city):
   if c_city == city:
          return "selected"
   return ""

@register.filter
def wichIndex(lists,index):
   list = lists[index]
   return list


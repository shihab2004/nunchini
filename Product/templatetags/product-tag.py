from django import template


register = template.Library()

@register.filter
def filter_image(object):
   image = object.product_image.get(is_main=True)

   return image.get_image()


@register.filter
def fast(obg):
   return obg[0]